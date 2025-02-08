from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None