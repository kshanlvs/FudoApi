from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from admin.schemas.add_product_schema import ProductCreate
from admin_model import Product, Category  # Ensure Category model is imported
from database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Check if the category exists
    category = db.query(Category).filter(Category.id == product.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Create the new product
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        image_url=product.image_url,
        category_id=product.category_id,  # Include category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully", "product": new_product}
