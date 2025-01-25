
from fastapi import FastAPI, HTTPException, Depends

from database import get_db
from models import User

from fastapi import  FastAPI
from sqlalchemy.orm import Session

from schemas import UserCreate

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


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