from fastapi import APIRouter, Depends, status
from app.configs.db import get_db
from app.services.get_current_user import get_current_user_by_token
from app.schemas.order_schema import OrderCreate
from app.controllers.order_controller import (
    create_order_controller,
    get_orders_controller
)

router = APIRouter()


@router.post("/create-order", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderCreate, db = Depends(get_db), current_user = Depends(get_current_user_by_token)):
    create_order_resp = await create_order_controller(order, db, current_user)
    return create_order_resp

@router.get("/get-orders", dependencies=[Depends(get_current_user_by_token)], status_code=status.HTTP_200_OK)
async def get_created_orders(db = Depends(get_db)):
    get_orders_resp = await get_orders_controller(db)
    return get_orders_resp
