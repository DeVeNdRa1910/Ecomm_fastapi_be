from fastapi import Depends, HTTPException, status
from jose import jwt
from app.configs.db import get_db
from app.configs.ENV import ENV_Config
from bson import ObjectId
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

JWT_SECRET_KEY = ENV_Config.JWT_SECRET_KEY
JWT_ALGORITHM = ENV_Config.JWT_ALGORITHM

security = HTTPBearer()

async def get_current_user_by_token(credentials: HTTPAuthorizationCredentials = Depends(security), db = Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=JWT_ALGORITHM)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invlid token")
        
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invlid token")
    
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    user["_id"] = str(user["_id"])
    
    return user