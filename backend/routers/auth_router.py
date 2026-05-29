from fastapi import APIRouter, Depends, HTTPException 
from sqlalchemy.orm import Session 
from pydantic import BaseModel, EmailStr 
from db import get_db 
from models.user_model import User 
from auth import get_password_hash, verify_password, create_access_token 

router = APIRouter() 

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="The email is already registered")
    new_user = User(
        username=data.username,
        email=data.email,
        password_hash=get_password_hash(data.password),
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User successfully registered", "user_id": new_user.id}

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(
    user_id=user.id,
    email=user.email
)

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }