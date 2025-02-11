from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
import os
import firebase_admin
from firebase_admin import credentials, storage
from admin.schemas.add_product_schema import ProductCreate, ProductsResponse
from admin_model import Product, Category  # Ensure Category model is imported
from database import get_db
from router.auth import check_admin  # Import JWT auth dependency

# Load Firebase credentials from environment variables



# Initialize Firebase (Ensure it's only initialized once)

firebase_credentials = {
    "type": "service_account",
    "project_id": os.getenv('FIREBASE_PROJECT_ID'),
    "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
    "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace("\\n", "\n"),
    "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
    "client_id": os.getenv('FIREBASE_CLIENT_ID'),
    "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
    "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
    "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_X509_CERT_URL'),
}

try:
    # Initialize Firebase Admin SDK
    cred = credentials.Certificate(firebase_credentials)
    firebase_admin.initialize_app(cred)  # Correct bucket domain

except Exception as e:
    print(f"❌ Firebase initialization failed: {e}")
router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    category_id: int = Form(...),
    image_file: UploadFile = File(None),  # Image is optional
    db: Session = Depends(get_db),
    is_admin: bool = Depends(check_admin)
):
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to create products"
        )

    # Check if category exists
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    # Upload image to Firebase Storage
    image_url = None
    if image_file:
        try:
            bucket = storage.bucket(name='sampe-cab22')
            blob = bucket.blob(f"product_images/{image_file.filename}")
            blob.upload_from_file(image_file.file, content_type=image_file.content_type)
            blob.make_public()
            image_url = blob.public_url
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(e)}")

    # Create new product
    new_product = Product(
        name=name,
        description=description,
        price=price,
        image_url=image_url,
        category_id=category_id
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return {"message": "Product added successfully", "product": new_product}


@router.get("/")
def fetch_all_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )

    products_response = [ProductsResponse.model_validate(product) for product in products]

    return {"products": products_response}


@router.get("/{product_id}", response_model=ProductsResponse)
def fetch_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product
