from fastapi import APIRouter, Depends, status, HTTPException
from app.configs.db import get_db

from app.services.get_current_user import get_current_user_by_token

router = APIRouter()

