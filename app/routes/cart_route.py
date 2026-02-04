from fastapi import APIRouter, Depends, status, Form
from app.configs.db import get_db
from app.schemas.cart_schema import (
    CartItemOut
)
from app.controllers.cart_controller import (
    add_product_in_cart_controller,
    get_cart_products_controller,
    remove_product_from_cart_controller, 
    delete_all_cart_product_controller,
    delete_one_product_controller
)
from app.services.get_current_user import get_current_user_by_token
from typing import List

router = APIRouter(dependencies=[Depends(get_current_user_by_token)])

@router.post("/add-product")
async def add_product_in_cart(product_id, db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    add_product_in_cart_resp = await add_product_in_cart_controller(product_id, db, current_user)
    return add_product_in_cart_resp


@router.get("/cart-products", response_model=List[CartItemOut])
async def get_cart_products(current_user = Depends(get_current_user_by_token), db = Depends(get_db)):
    get_cart_products_resp = await get_cart_products_controller(current_user, db)
    return get_cart_products_resp


@router.delete("/{product_id}")
async def delete_cart_product_by_one(product_id, db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    remove_product_from_cart_resp = await remove_product_from_cart_controller(product_id, db, current_user)
    return remove_product_from_cart_resp


@router.delete("/delete_all_products")
async def delete_all_products(current_user = Depends(get_current_user_by_token), db = Depends(get_db)):
    delete_all_cart_product_resp = await delete_all_cart_product_controller(current_user, db)
    return delete_all_cart_product_resp


@router.delete("/product/{product_id}")
async def delete_one_product(product_id, current_user = Depends(get_current_user_by_token), db = Depends(get_db)):
    delete_one_product_resp = await delete_one_product_controller(product_id, current_user, db)
    return delete_one_product_resp