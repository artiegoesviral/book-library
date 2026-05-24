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
    name: str
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):
    try:
        email = data.get("email")
        name = data.get("name")
        password = data.get("password")

        if not email or not name or not password:
            raise HTTPException(status_code=400, detail="Faltan campos obligatorios")

        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="El email ya está registrado")

        new_user = User(
            name=name,
            email=email,
            password=get_password_hash(password),
            is_admin=False
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}

    except HTTPException as e:
        raise e
    except Exception as e:
        # Captura errores inesperados
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# Login seguro
# Login

@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token(email=user.email, user_id=user.id, is_admin=user.is_admin)

    return {"access_token": token, 
            "token_type": "bearer",
            "is_admin": user.is_admin}

# Registro

@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
#Nuevo usuario
    new_user = User(
        name=data.name,
        email=data.email,
        password=get_password_hash(data.password),
        is_admin=False  # usuarios nuevos /no son admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Usuario registrado exitosamente", "user_id": new_user.id}