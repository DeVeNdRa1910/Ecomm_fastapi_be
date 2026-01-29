from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime, timezone
from typing import Optional
from enum import Enum
import re


class Product(BaseModel):
    product_name: str = Field(...)
    category: str = Field(...)
    