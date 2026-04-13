"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.config import settings

# Create database engine (use SQLite for testing, no DB server needed)
db_url = "sqlite:///./nids.db"  # Use SQLite instead of PostgreSQL
engine = create_engine(
    db_url,
    echo=settings.database_echo,
    future=True,
    connect_args={"check_same_thread": False}  # SQLite compatibility
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all models
Base = declarative_base()


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
