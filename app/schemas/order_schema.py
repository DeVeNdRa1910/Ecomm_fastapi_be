from pydantic import BaseModel, Field
from typing import List
from enum import Enum
from .product_schema import CategoryEnum

class PaymentStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    failed = "failed"
    refunded = "refunded"
    
class OrderFrom(str, Enum):
    cart = "cart"
    product_page = "product_page"

class OrderCreate(BaseModel):
    product_id: List[str] = Field(...)
    seller_id: List[str] = Field(...)
    ordered_from: OrderFrom = Field(...)
    user_id: str = Field(...)
    address: str = Field(...)
    quantity: int = Field(...)
    unit_price: float = Field(...)
    