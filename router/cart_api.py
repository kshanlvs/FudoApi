from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.cart_schema import CartItemResponse, CartItemCreate
from admin_model import Product
from database import get_db
from models import Cart
from router.auth import get_current_user  # Assuming check_admin is the dependency for checking JWT auth

router = APIRouter(prefix="/cart", tags=["Cart"])



@router.post("/add", response_model=CartItemResponse)
async def add_to_cart(
    cart_item: CartItemCreate,  # Request body will use CartItemCreate schema
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    # Check if the product exists
    product = db.query(Product).filter(Product.id == cart_item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if the product is already in the cart
    existing_cart_item = db.query(Cart).filter(Cart.user_id == current_user.id, Cart.product_id == cart_item.product_id).first()
    if existing_cart_item:
        # Update the quantity if the product already exists in the cart
        existing_cart_item.quantity += cart_item.quantity
        db.commit()
        db.refresh(existing_cart_item)
        return CartItemResponse(
            product_id=existing_cart_item.product_id,
            name=product.name,
            quantity=existing_cart_item.quantity,
            price=product.price,
            total=existing_cart_item.quantity * product.price
        )

    # Add a new cart item if not already in the cart
    new_cart_item = Cart(
        user_id=current_user.id,
        product_id=cart_item.product_id,
        quantity=cart_item.quantity,
        price=product.price
    )

    db.add(new_cart_item)
    db.commit()
    db.refresh(new_cart_item)

    return CartItemResponse(
        product_id=new_cart_item.product_id,
        name=product.name,
        quantity=new_cart_item.quantity,
        price=product.price,
        total=new_cart_item.quantity * product.price,
        image_url = product.image_url
    )


@router.get("/", response_model=dict)
async def get_cart_items(
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    cart_items = (
        db.query(Cart)
        .join(Product, Cart.product_id == Product.id)
        .filter(Cart.user_id == current_user.id)
        .all()
    )

    if not cart_items:
        raise HTTPException(status_code=404, detail="Cart is empty")

    cart_response = {
        "status": "success",
        "message": "Cart fetched successfully",
        "cart_items": [
            {
                "product_id": item.product_id,
                "name": item.product.name,
                "quantity": item.quantity,
                "price": item.price,
                "total": item.quantity * item.price,
                "image_url": item.product.image_url if item.product.image_url else None
            }
            for item in cart_items
        ]
    }

    return cart_response



