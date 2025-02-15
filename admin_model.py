from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    # Create a relationship to the Category model
    category = relationship("Category", back_populates="products")
    cart = relationship("Cart", back_populates="product", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = 'categories'  # Plural form for consistency

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)

    # Relationship back to the Product model
    products = relationship("Product", back_populates="category")
