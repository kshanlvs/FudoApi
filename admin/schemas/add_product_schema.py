# Pydantic Schema
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str | None = None

