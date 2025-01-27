from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate
from passlib.context import CryptContext

router = APIRouter(prefix="/users", tags=["users"])

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


@router.post("/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the email or phone already exists
    if db.query(User).filter((User.email == user.email) | (User.phone == user.phone)).first():
        raise HTTPException(status_code=400, detail="Email or phone already registered.")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Create a new User object
    new_user = User(
        name=user.name,
        email=user.email,
        phone=user.phone,
        password=hashed_password,
    )

    # Add to the database and commit
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully", "user_id": new_user.id}
