from fastapi import Depends, HTTPException

from fastapi.security import HTTPBearer
from fastapi.security import HTTPAuthorizationCredentials

from jose import jwt, JWTError

from sqlalchemy.orm import Session

from db import get_db

from auth import SECRET_KEY, ALGORITHM

from models.user_model import User

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        user_id = payload.get("user_id")

        if not user_id:
            raise HTTPException(status_code=401)

    except JWTError:
        raise HTTPException(status_code=401)

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401)

    return user