import os
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import Column, String, DateTime, Integer, text
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from jose import jwt

from database import engine, Base, get_db 

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secure-secret-key-change-this")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- ডাটাবেজ মডেল (TablePlus অনুযায়ী 'User') ---
class DBUser(Base):
    __tablename__ = "User" 
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    # Prisma-র 'createdAt' এর সাথে হুবহু মিল রাখা হয়েছে
    createdAt = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

# --- Pydantic স্কিমা ---
class UserCreate(BaseModel):
    name: Optional[str] = Field(None, max_length=100) 
    email: EmailStr
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: Optional[str]

# --- ইউটিলিটি ---
def wait_for_db():
    for _ in range(30):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                return
        except Exception:
            time.sleep(1)
    raise RuntimeError("Could not connect to the database")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@asynccontextmanager
async def lifespan(app: FastAPI):
    wait_for_db()
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title="Production Auth API", lifespan=lifespan)

# --- রাউটস ---
@app.post("/register", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.email == user.email).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="এই ইমেইলটি দিয়ে ইতিমধ্যে অ্যাকাউন্ট খোলা হয়েছে।"
        )
    
    hashed_password = pwd_context.hash(user.password)
    new_user = DBUser(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "রেজিস্ট্রেশন সফল হয়েছে", "user_id": new_user.id}

@app.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = db.query(DBUser).filter(DBUser.email == user_data.email).first()
    if not user or not pwd_context.verify(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="ইমেইল অথবা পাসওয়ার্ড সঠিক নয়।")
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer", "user_name": user.name}