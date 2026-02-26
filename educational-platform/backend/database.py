from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL

# Create database engine
engine = create_engine(DATABASE_URL, echo=False)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    # Dependency to provide database session to routes.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    # Create all tables in the database.
    Base.metadata.create_all(bind=engine)
