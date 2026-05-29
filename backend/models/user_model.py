from sqlalchemy import Column, Integer, String 
from pydantic import BaseModel, EmailStr 
from db import Base 

class User(Base): 
    __tablename__ = "users" 
    
    id = Column(Integer, primary_key=True, index=True) 
    username = Column(String(100), nullable=False) 
    email = Column(String(100), unique=True, nullable=False) 
    password_hash = Column(String(255), nullable=False)

class UserCreate(BaseModel): 
    username: str 
    email: EmailStr 
    password: str 

class UserLogin(BaseModel): 
    email: EmailStr 
    password: str 

class UserResponse(BaseModel): 
    id: int 
    username: str 
    email: EmailStr 
    is_admin: bool 

class Config: 
    from_attributes = True