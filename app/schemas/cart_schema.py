from pydantic import BaseModel, Field

class CartProduct(BaseModel):
    product_id: str = Field(...)
    
class CartProductInfo(BaseModel):
    id: str = Field(alias="_id")
    title: str
    description: str
    price: float
    seller_id: str
    product_image_urls: list[str]
    is_active: bool

    class Config:
        populate_by_name = True

    
class CartItemOut(BaseModel):
    id: str = Field(alias="_id")
    user_id: str
    quantity: int
    product: CartProductInfo
    
    class Config:
        populate_by_name = True