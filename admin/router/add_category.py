from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from admin.schemas.category_schema import CategoryCreate
from admin_model import Category
from database import get_db

router = APIRouter(prefix="/categories", tags=["Category"])

@router.post("/")
def create_product(category: CategoryCreate, db: Session = Depends(get_db)):
    new_category = Category(
        name=category.name,
        description=category.description,
        image_url=category.image_url,  # Include image URL
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"message": "Product added successfully", "product": new_category}
