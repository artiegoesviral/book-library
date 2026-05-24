from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext


SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def get_password_hash(password: str) -> str:
    """
    Recibe contraseña en texto plano y devuelve hash bcrypt.
    Se trunca a 72 bytes por limitación interna de bcrypt.
    """
    return pwd_context.hash(password[:72])


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifica contraseña en texto plano contra hash almacenado.
    """
    return pwd_context.verify(plain_password[:72], hashed_password)


from typing import Any, Dict, Optional


def create_access_token(payload: Optional[Dict[str, Any]] = None,
                        email: Optional[str] = None,
                        user_id: Optional[int] = None,
                        is_admin: bool = False) -> str:
    """
    Genera un token JWT. Acepta dos modos de uso:
    - `payload` (dict): cuando se pasa todo el payload ya formado.
    - `email` / `user_id` / `is_admin`: construcción explícita.

    Siempre añade `exp` y, si está disponible, `user_id`.
    """
    if payload is None:
        to_encode: Dict[str, Any] = {}
    else:
        to_encode = dict(payload)

    if email is not None:
        to_encode["sub"] = email

    if user_id is not None:
        to_encode["user_id"] = user_id

    to_encode["is_admin"] = is_admin or to_encode.get("is_admin", False)

    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)