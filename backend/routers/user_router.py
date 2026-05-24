from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import SessionLocal, get_db
from models.user_model import User
from schemas.user_schema import UserCreate, UserRead
from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_admin: bool
 
    class Config:
        from_attributes = True

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

