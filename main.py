
from fastapi import  HTTPException, Depends
from passlib.context import CryptContext
from starlette.middleware.cors import CORSMiddleware

from database import get_db
from models import User

from fastapi import  FastAPI
from sqlalchemy.orm import Session

from router.auth import get_current_user
from router.user_api import router as user_router
from router.login_api import router as login_router
from admin.router.add_product import router  as add_product
from admin.router.add_category import  router as add_category
from router.cart_api import  router as cart

from schema import UserCreate
from dotenv import load_dotenv
import os
from router.profile import router as profile_router

app = FastAPI()


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(add_product)
app.include_router(user_router)
app.include_router(profile_router)
app.include_router(add_category)
app.include_router(cart)

app.include_router(login_router)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}





# Load environment variables from .env file



def hash_password(password: str) -> str:
    return pwd_context.hash(password)

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "DB connection is working"}


@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(
            (User.email == user.email) | (User.phone == user.phone)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email or phone number already registered")

        # Hash password before saving
        hashed_password = hash_password(user.password)

        # Create new user
        new_user = User(
            name=user.name,
            email=user.email,
            phone=user.phone,
            password=hashed_password
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "phone": new_user.phone
        }

    except Exception as e:
        print(f"🔥 Error: {e}")  # Debugging log
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


