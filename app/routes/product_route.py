from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from app.configs.db import get_db
import cloudinary
from app.schemas.product_schema import (
    Inventory
)
from app.controllers.product_controller import (
    add_inventory_controller
)
from app.services.get_current_user import get_current_user_by_token
from typing import List, Annotated
import asyncio
from bson import ObjectId

router = APIRouter()

 
@router.post("/", status_code=201)
async def add_product_in_stock(
    title: str = Form(...), 
    description: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    quantity: int = Form(...),
    images: List[UploadFile] | None = File(None), 
    db = Depends(get_db), 
    current_user = Depends(get_current_user_by_token)
):
    
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to upload")
    
    if not images:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one image is required")
    
    product_image_secure_urls = []
    product_image_public_ids = []
    
    for product_image in images:
        if not product_image.content_type.startswith("image/"):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product picture must be an image")
        
        ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
        
        if product_image.content_type not in ALLOWED_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only JPEG, PNG and WEBP images are allowed")
        
        product_image_upload_result = await asyncio.to_thread(
            cloudinary.uploader.upload,
            product_image.file,
            folder="Fastapi_Ecommerce/Inventory/Product_images",
            resource_type="image"
        )
        
        product_image_secure_urls.append(product_image_upload_result["secure_url"])
        product_image_public_ids.append(product_image_upload_result["public_id"])
        
    product_data = Inventory(
        title=title, 
        description=description, 
        price=price, 
        category=category, 
        quantity=quantity, 
        seller_id=str(current_user["_id"]),
        product_image_urls=product_image_secure_urls,
        product_image_public_ids=product_image_public_ids
    )

    try:
        add_inventory_resp = await add_inventory_controller(product_data, db, current_user)
        return add_inventory_resp
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")