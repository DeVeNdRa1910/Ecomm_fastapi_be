from fastapi import HTTPException, status
from bson import ObjectId
from fastapi.encoders import jsonable_encoder


async def add_inventory_controller(data, db, current_user):
    product_data = data.model_dump()
    try:
        await db.inventory.insert_one(product_data)
        return {
            "message": f"{product_data["title"]} added successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Inventory not added: {e}")
    
    
async def get_seller_products_controller(current_user, db):
    
    try:
        seller_id = str(current_user["_id"])
        seller_products = await db.inventory.find({"seller_id": seller_id}).to_list(length=None)
        
        for product in seller_products:
            product["_id"] = str(product["_id"])
        
        return {
            "seller_products": seller_products
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to get the seller products: {e}")

async def get_seller_product_by_id_controller(product_id, current_user, db):
    try:
        get_product = await db.inventory.find_one({
            "_id": ObjectId(product_id),
            "seller_id": str(current_user["_id"])
        })
        
        if not get_product:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product not found")
        
        get_product["_id"] = str(get_product["_id"])
        
        return {
            "product": get_product
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch product: {e}")