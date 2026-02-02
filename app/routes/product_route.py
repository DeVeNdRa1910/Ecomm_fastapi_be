from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File, Form
from app.configs.db import get_db
import cloudinary
from app.schemas.product_schema import (
    Inventory,
    UpdateInventory, 
    CategoryEnum,
    ProductOut
)
from app.controllers.product_controller import (
    add_inventory_controller,
    get_seller_products_controller,
    get_seller_product_by_id_controller,
    get_all_products_controller, 
    delete_product_by_id_contorller, 
    update_inventory_controller,
    get_product_controller,
    get_product_by_category_controller,
)
from app.services.get_current_user import get_current_user_by_token
from typing import List, Optional
import asyncio
from bson import ObjectId

router = APIRouter()

 
@router.post("/", status_code=201)
async def add_product_in_stock(
    title: str = Form(...), 
    description: str = Form(...),
    price: float = Form(...),
    category: CategoryEnum = Form(...),
    quantity: int = Form(...),
    images: List[UploadFile] = File(), 
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
        is_active=True,
        seller_id=str(current_user["_id"]),
        product_image_urls=product_image_secure_urls,
        product_image_public_ids=product_image_public_ids
    )

    try:
        add_inventory_resp = await add_inventory_controller(product_data, db, current_user)
        return add_inventory_resp
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    
@router.get('/', status_code=200)
async def get_seller_products(current_user = Depends(get_current_user_by_token), db = Depends(get_db)):
    
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to perform this action")
    
    get_seller_products_resp = await get_seller_products_controller(current_user, db)
    return get_seller_products_resp 

@router.get("/selller/{product_id}")
async def get_seller_product_by_id(product_id, current_user = Depends(get_current_user_by_token), db = Depends(get_db)):
    
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You are not authorized to perform this action")
    
    get_product_resp = await get_seller_product_by_id_controller(product_id, current_user, db)
    return get_product_resp

@router.get("/all-products/", response_model=List[ProductOut])
async def get_all_products(db = Depends(get_db)):
    get_all_products_resp = await get_all_products_controller(db)
    return get_all_products_resp

@router.get('/{product_id}', response_model=ProductOut)
async def get_product_by_id(product_id, db = Depends(get_db)):
    get_product_resp = await get_product_controller(product_id, db)
    return get_product_resp

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product_by_id(product_id, current_user = Depends(get_current_user_by_token), db = Depends(get_db)):
    delete_product_by_id_resp = await delete_product_by_id_contorller(product_id, current_user, db)
    return delete_product_by_id_resp

@router.put("/{product_id}", status_code=201)
async def update_product_in_stock(
    product_id: str,
    title: Optional[str] = Form(None), 
    description: Optional[str] = Form(None),
    price: Optional[float] = Form(None),
    category: Optional[CategoryEnum] = Form(None),
    quantity: Optional[int] = Form(None),
    images: Optional[List[UploadFile]] = File(None), 
    db = Depends(get_db), 
    current_user = Depends(get_current_user_by_token)
):
    
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to upload")
    
    product_image_secure_urls = []
    product_image_public_ids = []
    
    if images:
        ALLOWED_TYPES = {"image/jpeg", "image/png", "image/webp"}
        
        for product_image in images:
            if not product_image.content_type.startswith("image/"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product picture must be an image")
            
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
        
    product_upadetd_data = UpdateInventory(
        title=title, 
        description=description, 
        price=price, 
        category=category, 
        quantity=quantity, 
        is_active=True, 
        seller_id=str(current_user["_id"]),
        product_image_urls=product_image_secure_urls if images else None,
        product_image_public_ids=product_image_public_ids if images else None,
    )
    
    try:
        update_inventory_resp = await update_inventory_controller(product_upadetd_data, product_id, db, current_user)
        return update_inventory_resp
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{e}")
    
@router.post("/by-category", response_model=List[ProductOut])
async def get_products_by_category(category: str = Form(), db = Depends(get_db)):
    get_product_by_category_resp = await get_product_by_category_controller(category, db)
    return get_product_by_category_resp