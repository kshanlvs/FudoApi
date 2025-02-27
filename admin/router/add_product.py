from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from sqlalchemy.orm import Session
import os
import firebase_admin
from firebase_admin import credentials, storage
from admin.schemas.add_product_schema import ProductCreate, ProductsResponse
from admin_model import Product, Category  # Ensure Category model is imported
from database import get_db
from models import Cart
from router.auth import check_admin, get_current_user  # Import JWT auth dependency
from PIL import Image
from io import BytesIO

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


from PIL import Image
from io import BytesIO
from fastapi import UploadFile, HTTPException

def compress_image(image_file: UploadFile) -> BytesIO:
    """Compress image while maintaining a 4:3 aspect ratio"""
    try:
        image = Image.open(image_file.file)
        image = image.convert("RGB")

        # Target width & height maintaining 4:3 aspect ratio
        target_width = 800
        target_height = int((4 / 3) * target_width)  # Ensures correct ratio (800x600)

        # Resize while maintaining aspect ratio
        image.thumbnail((target_width, target_height))

        # Save compressed image
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format="JPEG", quality=75)  # 75% quality for optimization
        img_byte_arr.seek(0)  # Reset stream position

        return img_byte_arr
    except Exception as error:
        raise HTTPException(status_code=500, detail=f"Error compressing image: {str(error)}")



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
            compressed_image = compress_image(image_file)
            bucket = storage.bucket(name='sampe-cab22')
            blob = bucket.blob(f"product_images/{image_file.filename}")
            blob.upload_from_file(compressed_image, content_type="image/jpeg")
            blob.make_public()
            image_url = blob.public_url
        except Exception as error:
            raise HTTPException(status_code=500, detail=f"Error uploading image: {str(error)}")

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



@router.get("/", response_model=dict)
async def get_products(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)  # Extract user ID securely
):
    """Fetch all products with cart quantity if present for the authenticated user."""

    # Fetch products with LEFT JOIN to include cart quantity
    products = (
        db.query(
            Product,
            Cart.quantity.label("cart_quantity")
        )
        .outerjoin(Cart, (Product.id == Cart.product_id) & (Cart.user_id == current_user.id))
        .all()
    )

    if not products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No products found"
        )

    # Construct response
    products_response = {
        "status": "success",
        "message": "Products fetched successfully",
        "products": [
            {
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "image_url": product.image_url if product.image_url else None,
                "description": product.description,
                "category": {
                    "id": product.category_id,
                    "name": product.category.name
                },
                "cart": {
                    "quantity": cart_quantity if cart_quantity else 0  # If not in cart, quantity = 0
                }
            }
            for product, cart_quantity in products
        ]
    }

    return products_response



@router.get("/{product_id}", response_model=ProductsResponse)
def fetch_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product
