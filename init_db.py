from database import Base, engine

# Create tables
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created.")
