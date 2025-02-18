from pydantic import BaseModel, PositiveInt
from typing import Optional

class CartItemCreate(BaseModel):
    product_id: int  # Product ID to be added to the cart
    quantity: PositiveInt  # Ensure quantity is always positive

    class Config:
        from_attributes = True  # Works with SQLAlchemy ORM models


class CartItemUpdate(BaseModel):
    product_id: int  # The product to update
    quantity: PositiveInt = 1  # Default decrement by 1, but allows custom decrement

    class Config:
        from_attributes = True


class CartItemResponse(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: float
    total: float
    image_url: Optional[str] = None  # Optional field for product image

    class Config:
        from_attributes = True  # Replaces `orm_mode = True` in Pydantic v2
