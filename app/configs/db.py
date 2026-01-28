from app.configs.ENV import ENV_Config
from motor.motor_asyncio import AsyncIOMotorClient
import certifi

client = AsyncIOMotorClient(
    ENV_Config.MONGODB_URI,
    tls=True,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=5000
)

db = client[ENV_Config.MONGO_DB]

# user_collection = db['users']

def get_db():
    return db

def close_db():
    client.close()


