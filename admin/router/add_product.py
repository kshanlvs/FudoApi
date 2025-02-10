from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from admin.schemas.add_product_schema import ProductCreate, ProductsResponse
from admin_model import Product, Category  # Ensure Category model is imported
from database import get_db
from router.auth import check_admin  # Import JWT auth dependency

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/")
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    is_admin: bool = Depends(check_admin)  # Check if user is admin
):
    if not is_admin:  # If check_admin returns False, deny access
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create products"
        )

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
        category_id=product.category_id,  # Associate with category
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully", "product": new_product}





@router.get("/",response_model=dict)
def fetch_all_products(
    db: Session = Depends(get_db),
):
    # Fetch all products from the database
    products = db.query(Product).all()

    # If no products are found, raise a 404 error
    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )

    # Prepare the products data in a dictionary format
    products_response = [ProductsResponse.model_validate(product) for product in products]


    # Return the list of all products in the dictionary format
    return {"products": products_response}


@router.get("/{product_id}",response_model=dict)
def fetch_product(
        product_id: int,
        db: Session = Depends(get_db),
):
    # Fetch the product by ID
    product = db.query(Product).filter(Product.id == product_id).first()

    # If the product doesn't exist, raise a 404 error
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Return the product data
    return {"product": product}
