from pydantic import BaseModel
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int  # Product ID to be added to the cart
    quantity: int  # Quantity of the product to add to the cart

    class Config:
        orm_mode = True

class CartItemResponse(BaseModel):
    product_id: int  # Product ID of the item in the cart
    name: str  # Product name
    quantity: int  # Quantity of the product in the cart
    price: float  # Price per unit of the product
    total: float  # Total price (quantity * price)

    class Config:
        orm_mode = True