"""
Database package initialization
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from .models.base import Base
import os
import logging
from pathlib import Path
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Create database directory
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)

# Database configuration
DB_FILE = DB_DIR / "support_chat.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_FILE}"

# Create engine with proper configuration
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True,
    pool_recycle=3600
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def init_db():
    """Initialize the database by creating all tables."""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}")
        raise

@contextmanager
def get_db():
    """Provide a database session context."""
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error: {str(e)}")
        raise
    finally:
        db.close()

def get_db_session():
    """Get a database session for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 