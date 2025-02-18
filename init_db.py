from database import Base, engine
from models import User
from admin_model import Product,Category
# Create tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")


