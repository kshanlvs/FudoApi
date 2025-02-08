
from fastapi import  HTTPException, Depends
from starlette.middleware.cors import CORSMiddleware

from database import get_db
from models import User

from fastapi import  FastAPI
from sqlalchemy.orm import Session

from router.user_api import router as user_router
from router.login_api import router as login_router
from admin.router.add_product import router  as add_product
from admin.router.add_category import  router as add_category
from schema import UserCreate
from dotenv import load_dotenv
import os
from router.profile import router as profile_router

app = FastAPI()


load_dotenv()

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

app.include_router(login_router)
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}





# Load environment variables from .env file
SECRET_KEY = os.getenv("SECRET_KEY")



@app.post("/users/", response_model=dict)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "name": new_user.name, "email": new_user.email}

@app.get("/users/{user_id}", response_model=dict)
def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": db_user.id, "name": db_user.name, "email": db_user.email}

@app.get("/allUsers", response_model=dict)
def get_all_user(db: Session = Depends(get_db)):
    # Fetch all users from the database
    db_users = db.query(User).all()

    # Check if there are users in the database
    if not db_users:
        raise HTTPException(status_code=404, detail="No users found")

    # Return users in dictionary format
    return {"users":"kishan"}
