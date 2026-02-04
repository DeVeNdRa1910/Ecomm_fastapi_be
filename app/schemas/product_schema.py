from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
from datetime import datetime, timezone
from typing import Optional, List
from enum import Enum
import re

class CategoryEnum(str, Enum):
    MOBILE_PHONES = "mobile_phones"
    LAPTOPS = "laptops"
    TABLETS = "tablets"
    DESKTOPS = "desktops"

    TELEVISIONS = "televisions"
    SMART_TVS = "smart_tvs"

    AUDIO_DEVICES = "audio_devices"  
    HOME_THEATRE = "home_theatre"

    CAMERAS = "cameras"
    WEARABLES = "wearables"  

    COMPUTER_ACCESSORIES = "computer_accessories"
    MOBILE_ACCESSORIES = "mobile_accessories"

    NETWORKING_DEVICES = "networking_devices"
    STORAGE_DEVICES = "storage_devices"

    GAMING_CONSOLES = "gaming_consoles"
    GAMING_ACCESSORIES = "gaming_accessories"

    SMART_HOME_DEVICES = "smart_home_devices"    


class Product(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    category: CategoryEnum = Field(...)
    is_active: bool = Field(...)
    
class Inventory(Product):
    seller_id: str = Field(...)
    quantity: int = Field(...)
    product_image_urls: List[str] = Field(default_factory=list)
    product_image_public_ids: List[str] = Field(default_factory=list)
    
    @computed_field
    @property
    def in_stock(self) -> bool :
        if self.quantity > 0:
            return True
        else:
            return False

class UpdateInventory(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category: Optional[CategoryEnum] = None
    seller_id: Optional[str] = None
    quantity: Optional[int] = None
    product_image_urls: Optional[List[str]] = None
    product_image_public_ids: Optional[List[str]] = None
    in_stock: bool = Field(...)
    is_active: Optional[bool] = None
    
class ProductOut(BaseModel):
    id: str = Field(alias="_id")
    title: str = Field(...)
    description: str = Field(...)
    price: float = Field(...)
    category: str = Field(...)
    seller_id: str = Field(...)
    product_image_urls: Optional[List[str]] =Field(...)
    is_active: bool = Field(...)
    in_stock: bool = Field(...)