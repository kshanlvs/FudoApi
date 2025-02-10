from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float  # Required field for product price
    image_url: str | None = None
    category_id: int

class ProductsResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None
    price: float
    category_id: int

    class Config:
        from_attributes = True