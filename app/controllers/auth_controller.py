from fastapi import HTTPException, status, Depends
from datetime import datetime, timezone
from app.schemas.auth_schema import RegisterUser, ChangePassword, ForgotPassword
from app.configs.password import get_hashed_password, verify_password 
from app.configs.Email import generate_otp, send_email, verify_otp, save_otp
from app.core.jwt_security import create_access_token
from bson import ObjectId
from fastapi.encoders import jsonable_encoder

async def resister_controller(data: RegisterUser, db):
    
    existing_user = await db.users.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exist")

    user_dict = data.model_dump()
    user_dict["is_verified"] = False
    user_dict['password'] = get_hashed_password(user_dict['password'])
    user_dict['created_at'] = datetime.now(timezone.utc)
    user_dict['updates_at'] = datetime.now(timezone.utc)
    
    try:
        resp = await db.users.insert_one(user_dict)
        
        
        created_user = await db.users.find_one({"_id": resp.inserted_id})
        
        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="User was created but could not be retrieved"
            )
            
        otp = generate_otp()
        send_email(user_dict["email"], str(otp))
        save_otp(user_dict["email"], str(otp))
        
        created_user["id"] = str(created_user["_id"])
        del created_user["_id"]
        del created_user["password"]
        
        return {
            "message": "OTP sent successfully"
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
        
async def resend_otp_controller(email: str, db):
    try:
        otp = generate_otp()
        send_email(email, str(otp))
        save_otp(email, str(otp))
        return {"message": "OTP resent successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_200_OK, detail="Unable to resend the otp")
    
        
async def verify_email(email: str, otp: str, db):
    if not verify_otp(email, otp):
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")
    
    try: 
        await db.users.update_one(
            {"email": email},
            {"$set": {"is_verified": True}}
        )
 
        return {
            "message": "Email verified successfully"
        }
        
    except Exception as e:
        raise ValueError("Email not verified")
    
        
async def login_controller(data:RegisterUser, db):
    
    user = await db.users.find_one({"email": data.email})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not user["is_verified"]:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email not verified")
    
    user_dict = data.model_dump()
    is_verified = verify_password(user_dict["password"], user["password"])
    
    if not is_verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invelid credentials")
    
    jwt_token = create_access_token({"sub": str(user["_id"]), "email": user["email"]})
    
    return {
        "access_token": jwt_token,
        "token_type": "bearer"
    }


async def change_password_controller(data: ChangePassword, current_user, db):
    if not verify_password(data.current_password, current_user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credential")
    
    new_hashed_password = get_hashed_password(data.new_password) 
    change_password_resp = await db.users.update_one({"_id": current_user["_id"]}, {"$set": {"password": new_hashed_password}})
    
    if change_password_resp.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password not updated") 
    
    return {
        "message": "Password updated successfully"
    }
    
async def forgot_password_otp_controller(data, db):
    user_existance = db.users.find_one({"email": str(data.email)})
    
    if not user_existance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    forgot_password_otp = generate_otp()
    send_email(data.email, str(forgot_password_otp))
    save_otp(data.email, str(forgot_password_otp))
    
    return {
        "message": "An otp has been sent on your resister email"
    }
    
async def forgot_password_controller(data: ForgotPassword, db):
    user_data = data.model_dump()
    
    if not verify_otp(user_data["email"], user_data["otp"]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired otp")
    
    get_new_hashed_password = get_hashed_password(str(user_data["new_password"]))
    
    try: 
        await db.users.update_one({"email": str(user_data["email"])}, {"$set": {"password": str(get_new_hashed_password)}})
        
        return {
            "message": "your password had been updated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password not updated")
    