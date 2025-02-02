import traceback
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from passlib.context import CryptContext
from jose import JWTError, jwt
from schemas.login import UserLogin
from dotenv import load_dotenv
import logging
import os
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

router = APIRouter(prefix="/users", tags=["authentication"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY is missing from environment variables")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize logger
logger = logging.getLogger(__name__)

# Helper function to verify passwords
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Helper function to create JWT token
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/login", response_model=dict)
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        # Query user by email or phone
        logger.info(f"Attempting to log in user with identifier: {user.identifier}")
        existing_user = db.query(User).filter(
            (User.email == user.identifier) | (User.phone == user.identifier)
        ).first()

        if not existing_user:
            logger.error(f"User with identifier {user.identifier} not found.")
            raise HTTPException(status_code=400, detail="User not found.")

        # Verify password
        if not verify_password(user.password, existing_user.password):
            logger.error(f"Invalid credentials for user with identifier: {user.identifier}")
            raise HTTPException(status_code=401, detail="Invalid credentials.")

        # Create JWT token
        access_token = create_access_token(data={"sub": str(existing_user.id)})
        logger.info(f"Login successful for user {user.identifier}, token generated.")

        return {"access_token": access_token, "token_type": "bearer"}

    except JWTError as jwt_error:
        logger.error(f"JWT error: {str(jwt_error)}")
        raise HTTPException(status_code=500, detail="JWT generation failed.")
    except Exception as e:
        logger.error(f"Unexpected error occurred during login: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail="Internal server error.")
