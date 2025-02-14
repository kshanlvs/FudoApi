from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)  # Added phone field
    password = Column(String, index=True)



class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))  # Assuming users table
    product_id = Column(Integer, ForeignKey('products.id'))  # Linking to products
    quantity = Column(Integer, default=1)
    price = Column(Float)  # You can store the product price in the cart

    user = relationship("User", back_populates="cart")
    product = relationship("Product", back_populates="cart")




