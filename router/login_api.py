from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from passlib.context import CryptContext

from schemas.login import UserLogin

router = APIRouter(prefix="/users", tags=["authentication"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Query user by email or phone
    existing_user = db.query(User).filter(
        (User.email == user.identifier) | (User.phone == user.identifier)
    ).first()

    if not existing_user:
        raise HTTPException(status_code=400, detail="User not found.")

    # Verify password
    if not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    return {"message": "Login successful", "user_id": existing_user.id}
