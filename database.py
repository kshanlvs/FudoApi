from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:ciJYamMAqdFQUNyIwLysHqUCSrNiHzDJ@viaduct.proxy.rlwy.net:19536/railway"

# Create the database engine
engine = create_engine(DATABASE_URL, echo=True)


# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
