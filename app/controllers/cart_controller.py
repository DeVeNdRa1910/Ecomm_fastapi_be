from fastapi import status, HTTPException
from bson import ObjectId


async def add_product_in_cart_controller(product_id, db, current_user):
    
    product = await db.inventory.find_one({"_id": ObjectId(product_id)})
    
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    
    if product["quantity"] < 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Product is Out of Stock ")
    
    try:
        await db.cartProduct.update_one(
            {
                "product_id": ObjectId(product_id),
                "user_id": current_user["_id"]
            },
            {
                "$inc": {"quantity": 1},
                "$setOnInsert": {
                    "product_id": ObjectId(product_id),
                    "user_id": current_user["_id"]
                }
            },
            upsert=True
        )
        
        return {
            "message": "Product added in your cart."
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to add product in cart: {e}")
    
    
async def get_cart_products_controller(current_user, db):
    
    pipeline = [
        {
            "$match": {
                "user_id": current_user["_id"]
            }
        },
        {
            "$lookup": {
                "from": "inventory",
                "localField": "product_id",
                "foreignField": "_id",
                "as": "product"
            }
        },
        {
             "$unwind": "$product"
        }
    ]
    
    try:
        cart_products = await db.cartProduct.aggregate(pipeline).to_list(length=None)
        if not cart_products:
            return []
        
        for item in cart_products:
            item["_id"] = str(item["_id"])
            item["product_id"] = str(item["product_id"])
            item["user_id"] = str(item["user_id"])
            item["product"]["_id"] = str(item["product"]["_id"])
        
        return cart_products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch cart products: {e}")
    
    
async def remove_product_from_cart_controller(product_id, db, current_user):
    
    try:
        result = await db.cartProduct.update_one(
            {
                "product_id": ObjectId(product_id),
                "user_id": current_user["_id"],
                "quantity": {"$gt": 1}    
            },
            {
                "$inc": {"quantity": -1}
            }
        )
        
        if result.modified_count:
            return {
                "message": "Product removed decreased"
            }
        
        await db.cartProduct.delete_one(
            {
                "product_id": ObjectId(product_id),
                "user_id": current_user["_id"],
                "quantity": 1   
            }
        )
        
        return {"message": "Product removed from cart"}
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to delete the product from your cart: {e}")
    
    
async def delete_all_cart_product_controller(current_user, db):
    try:
        await db.cartProduct.delete_many({"user_id": current_user["_id"]})
        return {
            "message": "All products has been removed from the cart."
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"failed to remove all the products from the cart: {e}")
    
    
async def delete_one_product_controller(product_id, current_user, db):
    try:
        await db.cartProduct.delete_many({"product_id": ObjectId(product_id)})
        return {
            "message": "Product removed"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to delete the product from the cart: {e}")