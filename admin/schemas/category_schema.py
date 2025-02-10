from pydantic import BaseModel

class CategoryCreate(BaseModel):
    name: str
    description: str | None = None
    image_url: str | None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    image_url: str | None = None

    class Config:
        from_attributes = True