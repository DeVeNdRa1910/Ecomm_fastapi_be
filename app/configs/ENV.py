from dotenv import load_dotenv
import os

load_dotenv()

class ENV_Config():
    MONGODB_URI = os.getenv("MONGODB_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    
    EMAIL_HOST=os.getenv("EMAIL_HOST")
    EMAIL_PORT=os.getenv("EMAIL_PORT")
    EMAIL_USER=os.getenv("EMAIL_USER")
    EMAIL_PASS=os.getenv("EMAIL_PASS")
    
    JWT_SECRET_KEY=os.getenv("SECRET_KEY")
    JWT_ALGORITHM=os.getenv("ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
    
    CLOUDINARY_CLOUD_NAME=os.getenv("CLOUDINARY_CLOUD_NAME")
    CLOUDINARY_API_KEY=os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRET=os.getenv("CLOUDINARY_API_SECRET")