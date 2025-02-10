from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from admin.schemas.category_schema import CategoryCreate, CategoryResponse
from admin_model import Category
from database import get_db
from router.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Category"])

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Ensure JWT authentication
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    new_category = Category(
        name=category.name,
        description=category.description,
        image_url=category.image_url,  # Include image URL
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"message": "Category Added Successfully", "category": new_category}


@router.get("/", response_model=dict)  # Define the response model as dict
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    if not categories:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No categories found"
        )

    # Use CategoryResponse to serialize the list of categories
    categories_response = [CategoryResponse.Config.from_attributes(category) for category in categories]

    return {"categories": categories_response}