from pydantic import BaseModel, Field
from typing import List

class StripeSessionResponse(BaseModel):
    url: str = Field()
    
class ProductDetails(BaseModel):
    product_name: str
    product_price: float
    quantity: int

class StripeCreateSession(BaseModel):
    product_details : List[ProductDetails]