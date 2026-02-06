from fastapi import APIRouter, Depends, status, HTTPException
from app.configs.db import get_db
from app.services.get_current_user import get_current_user_by_token
from app.schemas.order_schema import OrderCreate
from app.controllers.order_controller import (
    create_order_controller,
    get_orders_controller, 
    get_user_for_sellers_controllers,
    export_seller_users_controller,
    get_monthly_growth_controller
)

router = APIRouter()


@router.post("/create-order", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    create_order_resp = await create_order_controller(order, db, current_user)
    return create_order_resp

@router.get("/get-orders", status_code=status.HTTP_200_OK)
async def get_created_orders(db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    get_orders_resp = await get_orders_controller(db, current_user)
    return get_orders_resp

@router.get("/get-user", status_code=status.HTTP_200_OK)
async def get_users_for_seller(db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to use this endpoint")
    get_users_resp = await get_user_for_sellers_controllers(current_user, db)
    return get_users_resp

@router.get("/seller/users/export", status_code=status.HTTP_200_OK)
async def export_seller_users(db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    export_seller_users_resp = await export_seller_users_controller(db, current_user)
    return export_seller_users_resp


@router.get("/seller/growth", status_code=status.HTTP_200_OK)
async def get_monthly_growth(db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    if current_user["role"] != "seller":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to user this endpoint")
    get_monthly_growth_resp = await get_monthly_growth_controller(db, current_user)
    return get_monthly_growth_resp