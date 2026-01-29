from fastapi import APIRouter, Depends, status, UploadFile, File, HTTPException, Form
from app.configs.db import get_db

from app.schemas.user_schema import (
    UserInfoPost
)
from app.controllers.user_controller import (
    logged_in_user_info,
    update_user_profile_controller,
)
from app.services.get_current_user import get_current_user_by_token
import cloudinary.uploader
from typing import Optional
import asyncio

router = APIRouter()

@router.get("/me")
async def get_me(current_user=Depends(get_current_user_by_token), db=Depends(get_db)):
    get_me_resp = await logged_in_user_info(current_user, db)
    return get_me_resp


@router.put("/me")
async def update_user_profile(
    name: Optional[str] = Form(None),
    email: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    first_name: Optional[str] = Form(None),
    last_name: Optional[str] = Form(None),
    mobile_number: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None),
    current_user=Depends(get_current_user_by_token),
    db=Depends(get_db),
):
    
    user_data = {
        "name": name,
        "email": email,
        "address": address,
        "first_name": first_name,
        "last_name": last_name,
        "mobile_number": mobile_number,
    }
    
    if profile_image:
        
        if not profile_image.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile picture must be an image")
        
        if current_user.profile_image is not None:
            await asyncio.to_thread(
                cloudinary.uploader.destroy,
                current_user.public_id
            )
        
        profile_image_upload_result = await asyncio.to_thread(
            cloudinary.uploader.upload,
            profile_image.file,
            folder="Fastapi_Ecommerce/Userinfo/Profile_images",
            resource_type="image"
        )
        
        user_data["profile_image"] = profile_image_upload_result["secure_url"]
        user_data["public_id"] = profile_image_upload_result["public_id"]
     
    update_user_profile_resp = await update_user_profile_controller(user_data, current_user, db)
    return update_user_profile_resp