from pydantic import BaseModel
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int  # Product ID to be added to the cart
    quantity: int  # Quantity of the product to add to the cart

    class Config:
        orm_mode = True


class CartItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float
    total: float
    image_url: str  # Add image field

    class Config:
        from_attributes = True