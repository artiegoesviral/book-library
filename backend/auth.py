import os

from dotenv import load_dotenv

from datetime import datetime, timedelta

from jose import jwt

from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: int, email: str):

    payload = {
        "user_id": user_id,
        "sub": email,
        "exp": datetime.utcnow() + timedelta(minutes=60)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)