from jose import jwt
from datetime import datetime, timezone, timedelta
from app.configs.ENV import ENV_Config

JWT_SECRET_KEY = ENV_Config.JWT_SECRET_KEY
JWT_ALGORITHM = ENV_Config.JWT_ALGORITHM
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = ENV_Config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    data.update({'exp': expire})
    return jwt.encode(data, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)