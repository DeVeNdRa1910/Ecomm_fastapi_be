from fastapi import HTTPException, status
from app.schemas.order_schema import OrderCreate
from datetime import datetime, timezone
from app.schemas.order_schema import (
    PaymentStatus
)
from bson import ObjectId

async def create_order_controller(order: OrderCreate, db, current_user):
    try:
        order_data = order.model_dump()
        order_data["user_id"] = ObjectId(current_user["_id"])
        order_data["payment_status"] = PaymentStatus.pending
        order_data["created_at"] = datetime.now(timezone.utc)
        order_data["product_id"] = [ ObjectId(pid) for pid in order_data["product_id"] ]
        order_data["seller_id"] = [ ObjectId(sid) for sid in order_data["seller_id"] ]
        
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

async def get_orders_controller(db, current_user):
    pipeline = [
        {
            "$match": {
                "user_id": ObjectId(current_user["_id"])
            }
        },

        {
            "$lookup": {
                "from": "inventory",
                "localField": "product_id", 
                "foreignField": "_id",
                "as": "products"
            }
        },

        {
            "$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }
        },
        
        {"$unwind": "$user"},

        

       {
            "$project": {
                "_id": 0,
                "order_id": {"$toString": "$_id"},
                "user_name": "$user.name",
                "is_delivered": 1,
                "address": 1,
                "payment_status": 1,
                "quantity": 1,
                "unit_price": 1,
                "created_at": 1,
                
                "products": {
                    "$map": {
                        "input": "$products",
                        "as": "p",
                        "in": {
                        "_id": {"$toString": "$$p._id"},
                        "title": "$$p.title",
                        "price": "$$p.price",
                        "product_image_urls": "$$p.product_image_urls"
                        }
                    }
                }
            }
        },
        
        {
            "$sort": {"created_at": -1}
        }
    ]
    
    try:
        orders = await db.order.aggregate(pipeline).to_list(length=None)
        
        if not orders:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order are not availables")
        
        return orders
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to get orders: {e}")