from database import Base, engine
from models import User
# Create tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
