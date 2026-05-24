from fastapi import HTTPException
from db import get_conexion
from models.user_model import UserCreate, UserLogin
import db as Base
from auth import hash_password, verify_password, create_token


async def register(user: UserCreate):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(Base.DictCursor) as cursor:
            hashed_pass = hash_password(user.password)
            
            # INSERT corregido (solo 5 placeholders)
            await cursor.execute(
                "INSERT INTO users (name, email, password, role, is_active) VALUES (%s,%s,%s,%s,%s)",
                (
                    user.name,
                    user.email,
                    hashed_pass,
                    user.is_admin
                ),
            )
            await conn.commit()
            
            new_id = cursor.lastrowid
            
            # Obtener el usuario insertado
            await cursor.execute(
                "SELECT * FROM users WHERE id=%s", (new_id,)
            )
            new_user = await cursor.fetchone()
            
            return {"msg": "Usuario registrado correctamente", "item": new_user}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            await conn.close()


async def login(user_login: UserLogin):
    conn = None
    try:
        conn = await get_conexion()
        async with conn.cursor(Base.DictCursor) as cursor:
            # Campo correcto: email
            await cursor.execute(
                "SELECT * FROM users WHERE email=%s", (user_login.email,)
            )
            user = await cursor.fetchone()
            if not user:
                raise HTTPException(
                    status_code=404, detail="Usuario o password incorrecto"
                )

            # Verificar la contraseña
            if not verify_password(user_login.password, user["password"]):
                raise HTTPException(
                    status_code=404, detail="Usuario o password incorrecto"
                )

            # Crear token
            token_data = {"id": user["id"], "email": user["email"]}
            token = create_token(token_data)

            return {"msg": "Usuario logado correctamente", "token": token}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        if conn:
            await conn.close()