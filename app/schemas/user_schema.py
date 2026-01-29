from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserInfoPost(BaseModel):
    first_name: Optional[str] = Field(None, min_length=4, max_length=30)
    last_name: Optional[str] = Field(None, min_length=4, max_length=30)
    mobile_number: Optional[str] = Field(None, min_length=10, max_length=18)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, min_length=12)
    profile_image: Optional[str] = None