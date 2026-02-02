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
    
    
async def get_all_products_controller(db):
    
    try: 
        all_products = await db.inventory.find({"is_active": True}).to_list(length=None)
        
        if not all_products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Active products are not available")
        
        for product in all_products:
            product["_id"] = str(product["_id"])
        
        return all_products
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch products: {e}")
    
async def delete_product_by_id_contorller(product_id, current_user, db):
    try:
        product = await db.inventory.find_one({"_id": ObjectId(product_id)})
        
        if not product:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found.")
        
        if product["seller_id"] != current_user["_id"]:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to delete this product.")
        
        await db.inventory.delete_one({"_id": ObjectId(product_id)})
        
        return {
            "message": "Product with deleted successfully."
        }
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to delete product: {e}")

async def update_inventory_controller(data, product_id, db, current_user):
    product_data = data.model_dump(exclude_none=True)
    
    existed_product = await db.inventory.find_one({"_id": ObjectId(product_id)})

    if not existed_product:
        raise HTTPException(404, "Product not found")

    if existed_product["seller_id"] != str(current_user["_id"]):
        raise HTTPException(401, "You are not authorized")
    
    try:
        product_update_result = await db.inventory.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
        
        if product_update_result.matched_count == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
        
        return {
            "message": f"Product updated successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Inventory not added: {e}")
    
    
async def get_product_controller(product_id, db):
    try: 
        product = await db.inventory.find_one({"_id": ObjectId(product_id)})
        
        if not product: 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producut not found")
        
        product["_id"] = str(product["_id"])
        return product

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch the product: {e}")
    
    
async def get_product_by_category_controller(category, db):
    try:
        category_products = await db.inventory.find({"category": category}).to_list(length=None)
        if not category_products:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not available")
        
        for product in category_products:
            product["_id"] = str(product["_id"])
        
        return category_products
    
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed to fetch product by category: {e}")