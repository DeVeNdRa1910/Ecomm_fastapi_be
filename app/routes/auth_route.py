from fastapi import APIRouter, Depends, status, HTTPException
from app.configs.db import get_db
from app.schemas.auth_schema import (
    RegisterUser,
    UserResponse,
    LoginUser,
    OtpValidator,
    ChangePassword,
    ForgotPassword,
    OtpForgotPassword,
)
from app.controllers.auth_controller import (
    resister_controller,
    login_controller,
    verify_email,
    resend_otp_controller,
    change_password_controller,
    forgot_password_otp_controller,
    forgot_password_controller,
)
from app.services.get_current_user import get_current_user_by_token

router = APIRouter()


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def register_user(data: RegisterUser, db=Depends(get_db)):
    register_resp = await resister_controller(data, db)
    return register_resp


@router.post("/verify_email", status_code=status.HTTP_201_CREATED)
async def verify_email_by_otp(data: OtpValidator, db=Depends(get_db)):
    verify_email_resp = await verify_email(data.email, data.otp, db)
    return verify_email_resp


@router.get("/resend_otp", status_code=status.HTTP_200_OK)
async def resend_otp(email: str, db=Depends(get_db)):
    resend_otp_resp = await resend_otp_controller(email, db)
    return resend_otp_resp 


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(data: LoginUser, db=Depends(get_db)):
    login_resp = await login_controller(data, db)
    return login_resp


@router.post("/change-password", status_code=status.HTTP_201_CREATED)
async def change_password(
    data: ChangePassword,
    current_user=Depends(get_current_user_by_token),
    db=Depends(get_db),
):
    change_password_resp = await change_password_controller(data, current_user, db)
    return change_password_resp


@router.post("/get_forgot_password_otp", status_code=status.HTTP_200_OK)
async def forgot_password_otp(data: OtpForgotPassword, db=Depends(get_db)):
    forgot_password_otp_resp = await forgot_password_otp_controller(data, db)
    return forgot_password_otp_resp


@router.post("/forgot-password", status_code=status.HTTP_201_CREATED)
async def forgot_password(data: ForgotPassword, db=Depends(get_db)):
    forgot_password_resp = await forgot_password_controller(data, db)
    return forgot_password_resp
