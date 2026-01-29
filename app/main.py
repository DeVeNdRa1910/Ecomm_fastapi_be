from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import auth_route, userinfo_route
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.configs.db import get_db, close_db
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@asynccontextmanager
async def lifespan(app: FastAPI):
    db = get_db()
    await db.command("ping")
    print("MongoDB connected")

    yield

    close_db()
    print("🛑 MongoDB connection closed")

load_dotenv()

origins = ["http://localhost","http://localhost:3000"]

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)

@app.get("/", tags=["health"])
def helth():
    return {"message": "Server is UP and RUNNING"}

app.include_router(auth_route.router, prefix="/auth", tags=["Authentication"])
app.include_router(userinfo_route.router, prefix="/user", tags=["User Info"])