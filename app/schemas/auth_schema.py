from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import re

# An Enum (Enumeration) is a fixed set of allowed values. Instead of allowing any string or number, you restrict the input to known options only.

class RolesEnum(str, Enum):
    seller = "seller"
    buyer = "buyer"

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RolesEnum = RolesEnum.buyer
    is_verified: bool = False
    
    
    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if not value.strip():
            raise ValueError("name field can't be empty")
        if len(value) < 4:
            raise ValueError("name field should have at least 4 characters")
        return value


class RegisterUser(BaseModel):
    name: str
    email: EmailStr
    role: RolesEnum = RolesEnum.buyer
    password: str = Field(min_length=8, max_length=20)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password field can't be empty")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password should contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password should contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password should contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password should contain at least one special(!@#$%^&*(),.?\":{}|<>) character")
        return value
    
class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=20)
    
    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password field can't be empty")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password should contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password should contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password should contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password should contain at least one special(!@#$%^&*(),.?\":{}|<>) character")
        return value

class UserResponse(BaseModel):
    message: str

class OtpValidator(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6)
    
class ChangePassword(BaseModel):
    current_password: str = Field(min_length=8, max_length=20)
    new_password: str = Field(min_length=8, max_length=20)
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password field can't be empty")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password should contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password should contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password should contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password should contain at least one special(!@#$%^&*(),.?\":{}|<>) character")
        return value
    
class OtpForgotPassword(BaseModel):
    email: EmailStr
    
class ForgotPassword(BaseModel):
    email: EmailStr
    otp: str
    new_password: str = Field(min_length=8, max_length=20)
    
    @field_validator("new_password")
    @classmethod
    def validate_password(cls, value):
        if not value.strip():
            raise ValueError("Password field can't be empty")
        if not re.search(r"[a-z]", value):
            raise ValueError("Password should contain at least one lowercase letter")
        if not re.search(r"[A-Z]", value):
            raise ValueError("Password should contain at least one uppercase letter")
        if not re.search(r"\d", value):
            raise ValueError("Password should contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError("Password should contain at least one special(!@#$%^&*(),.?\":{}|<>) character")
        return value