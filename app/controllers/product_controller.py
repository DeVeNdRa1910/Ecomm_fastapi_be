from fastapi import HTTPException, status, Depends
from datetime import datetime, timezone
from app.schemas.auth_schema import RegisterUser, ChangePassword, ForgotPassword
from app.configs.password import get_hashed_password, verify_password 
from app.configs.Email import generate_otp, send_email, verify_otp, save_otp
from app.core.jwt_security import create_access_token
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


async def add_inventory_controller(data, db, current_user):
    product_data = data.model_dump()
    try:
        await db.inventory.insert_one(product_data)
        return {
            "message": f"{product_data["title"]} added successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Inventory not added: {e}")
