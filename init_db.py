from database import Base, engine
from models import User
from models import Product
# Create tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
