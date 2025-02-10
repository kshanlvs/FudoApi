from pydantic import BaseModel
from fastapi import File, UploadFile



class ProductCreate(BaseModel):
    name: str
    description: str | None = None
    price: float  # Required field for product price
    image_file: UploadFile = File(None)
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