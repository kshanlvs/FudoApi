from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from schemas.login import UserLogin
from dotenv import load_dotenv
import logging
import os


load_dotenv()
router = APIRouter(prefix="/users", tags=["authentication"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



 # Load environment variables from .env file
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

logger = logging.getLogger(__name__)

@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Query user by email or phone
    logger.info("Attempting to log in user.")
    existing_user = db.query(User).filter(
        (User.email == user.identifier) | (User.phone == user.identifier)
    ).first()

    if not existing_user:
        logger.error("User not found.")
        raise HTTPException(status_code=400, detail="User not found.")

    # Verify password
    if not verify_password(user.password, existing_user.password):
        logger.error("Invalid credentials.")

        raise HTTPException(status_code=401, detail="Invalid credentials.")

    # Create JWT token
    access_token = create_access_token(data={"sub": str(existing_user.id)})
    logger.info("Login successful, token generated.")

    return {"access_token": access_token, "token_type": "bearer"}
