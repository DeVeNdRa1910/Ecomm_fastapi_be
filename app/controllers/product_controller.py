from fastapi import HTTPException, status, Depends
from datetime import datetime, timezone
from app.schemas.auth_schema import RegisterUser, ChangePassword, ForgotPassword
from app.configs.password import get_hashed_password, verify_password 
from app.configs.Email import generate_otp, send_email, verify_otp, save_otp
from app.core.jwt_security import create_access_token
from bson import ObjectId
from fastapi.encoders import jsonable_encoder