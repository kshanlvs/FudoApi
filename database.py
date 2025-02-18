from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Use connection pooling settings to optimize database performance
DATABASE_URL = "postgresql://postgres:QbicKrEIqJfTGxnrAEKpWdeLIAWROUhz@junction.proxy.rlwy.net:37908/railway"

# Create the engine with connection pooling configurations
engine = create_engine(
    DATABASE_URL,
    echo=True,
    pool_size=20,           # Number of connections to keep in the pool
    max_overflow=10,        # How many connections to allow beyond the pool size
    pool_timeout=30,        # Timeout in seconds before raising an exception
    pool_recycle=3600       # Recycle connections after this many seconds
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = None
    try:
        db = SessionLocal()
        print("✅ Database session created!")
        yield db
    except Exception as e:
        if db:
            db.rollback()  # Rollback in case of any exception
        print(f"🔥 Error getting DB session: {e}")
        raise HTTPException(status_code=500, detail=f"Database session failed {e}")
    finally:
        if db:
            db.close()  # Ensure session is closed after usage
            print("✅ Database session closed.")
