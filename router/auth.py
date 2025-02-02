from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from models import User
from sqlalchemy.orm import Session
import os

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
