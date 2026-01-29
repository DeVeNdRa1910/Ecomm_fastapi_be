from fastapi import HTTPException, status, Depends
from datetime import datetime, timezone
from app.schemas.auth_schema import RegisterUser, ChangePassword, ForgotPassword
from app.configs.password import get_hashed_password, verify_password 
from app.configs.Email import generate_otp, send_email, verify_otp, save_otp
from app.core.jwt_security import create_access_token
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


async def logged_in_user_info(current_user, db):
    user_id = ObjectId(current_user["_id"])
    
    current_user = await db.users.find_one({"_id": user_id})
    
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    current_user["_id"] = str(current_user["_id"])
    
    del current_user["password"]
    del current_user["_id"]
    
    return jsonable_encoder(current_user)

async def update_user_profile_controller(user_data, current_user, db):
    
    try:
        update_data = {}
        
        allowed_fields = [
            "first_name",
            "last_name",
            "mobile_number",
            "email",
            "profile_image",
            "address",
        ]
        
        for field in allowed_fields:
            if field in user_data and user_data[field] is not None:
                update_data[field] = user_data[field]

        if not update_data:
            return {"message": "No fields to update"}
          
        profile_update_result = await db.users.update_one({"email": str(current_user["email"])}, {"$set": update_data})

        if profile_update_result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "message": "User profile updated successfully"
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail="Something went wrong, Try after sometime")