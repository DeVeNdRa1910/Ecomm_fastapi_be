import cloudinary
from app.configs.ENV import ENV_Config

cloudinary.config( 
  cloud_name = ENV_Config.CLOUDINARY_CLOUD_NAME, 
  api_key = ENV_Config.CLOUDINARY_API_KEY, 
  api_secret = ENV_Config.CLOUDINARY_API_SECRET, 
  secure=True
)