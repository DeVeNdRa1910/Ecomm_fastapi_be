from fastapi import HTTPException, status
from app.schemas.order_schema import OrderCreate
from datetime import datetime, timezone
from app.schemas.order_schema import (
    PaymentStatus
)

async def create_order_controller(order: OrderCreate, db, current_user):
    try:
        order_data = order.model_dump()
        order_data["user_id"] = current_user["_id"]
        order_data["payment_status"] = PaymentStatus.pending
        order_data["created_at"] = datetime.now(timezone.utc)
        
        order_create_resp = await db.order.insert_one(order_data)
        print(order_create_resp)
        
        if getattr(order, "ordered_from", None) == "cart":
            await db.cartProduct.delete_many({"user_id": current_user["_id"] })
        
        return {
            "message": "Order created successfully",
            "order_id": str(order_create_resp.inserted_id)
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to create the order: {e}")

async def get_orders_controller(db):
    
    pass