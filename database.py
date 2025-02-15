from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# DATABASE_URL = "postgresql://postgres:ciJYamMAqdFQUNyIwLysHqUCSrNiHzDJ@viaduct.proxy.rlwy.net:19536/railway" production
DATABASE_URL = "postgresql://postgres:QbicKrEIqJfTGxnrAEKpWdeLIAWROUhz@junction.proxy.rlwy.net:37908/railway"

engine = create_engine(DATABASE_URL, echo=True)


# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    try:
        db = SessionLocal()
        print("✅ Database session created!")
        yield db
    except Exception as e:
        print(f"🔥 Error getting DB session: {e}")
        raise HTTPException(status_code=500, detail=f"Database session failed {e}")
