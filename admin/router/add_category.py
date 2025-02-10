from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from admin.schemas.category_schema import CategoryCreate, CategoryResponse
from admin_model import Category
from database import get_db
from router.auth import check_admin  # Import admin authentication

router = APIRouter(prefix="/categories", tags=["Category"])

@router.post("/")
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(check_admin)  # Ensure admin authentication
):
    if not is_admin:  # If the user is not an admin, deny access
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create categories"
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
    categories_response = [CategoryResponse.model_validate(category) for category in categories]

    return {"categories": categories_response}
