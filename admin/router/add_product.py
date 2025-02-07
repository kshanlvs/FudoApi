from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from admin.schemas.add_product_schema import ProductCreate
from models import Product
from database import get_db

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        description=product.description,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product added successfully", "product": new_product}
