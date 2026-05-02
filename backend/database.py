"""
Database connection and models for MySQL.

Sprint P3.2: Database + Summary Persistence
- Uses SQLAlchemy with aiomysql for async operations
- Password hashing with bcrypt (already implemented in auth.py)
"""

import logging
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Boolean,
    Enum as SQLEnum,
)
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func

from .config import settings

# Configure logging
logger = logging.getLogger("backend.database")


# ============================================
# SQLAlchemy Base
# ============================================

class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


# ============================================
# Database Models
# ============================================

class User(Base):
    """
    User model for authentication.
    
    Passwords are stored as bcrypt hashes (not plain text).
    The hash_password function in auth.py handles the hashing.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), nullable=True)
    password = Column(String(255), nullable=False)  # bcrypt hash
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    summaries = relationship("Summary", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(id={self.id}, email={self.email})>"


class Summary(Base):
    """
    Summary model for storing video summaries.
    
    Links to User via foreign key for user-specific history.
    """
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    video_id = Column(String(50), nullable=False, index=True)
    video_title = Column(String(500), nullable=False)
    video_url = Column(String(500), nullable=True)
    video_channel = Column(String(255), nullable=True)
    
    # Transcript stats (stored as JSON string for simplicity)
    transcript_language = Column(String(10), nullable=True)
    transcript_word_count = Column(Integer, nullable=True)
    transcript_duration = Column(Integer, nullable=True)
    
    # LLM provider used
    llm_provider = Column(String(50), nullable=True)
    llm_model = Column(String(100), nullable=True)
    
    # Summary content
    summary_text = Column(Text, nullable=False)
    
    # Metadata
    created_at = Column(DateTime, default=func.now(), nullable=False, index=True)
    
    # Relationships
    user = relationship("User", back_populates="summaries")
    
    def __repr__(self):
        return f"<Summary(id={self.id}, user_id={self.user_id}, video_id={self.video_id})>"


# ============================================
# Database Engine and Session
# ============================================

# Create async engine
engine = create_async_engine(
    settings.database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    """
    Dependency for getting database session.
    
    Usage:
        @app.get("/endpoint")
        async def endpoint(db: AsyncSession = Depends(get_db)):
            ...
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Initialize database tables."""
    from sqlalchemy import text
    from sqlalchemy.ext.asyncio import AsyncEngine
    
    logger.info("Initializing database tables...")
    
    # Import all models to ensure they're registered
    # (User and Summary are already imported above)
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")


async def close_db():
    """Close database connections."""
    logger.info("Closing database connections...")
    await engine.dispose()
    logger.info("Database connections closed")


# ============================================
# Sync Engine (for migrations/CLI tools)
# ============================================

sync_engine = create_engine(
    settings.sync_database_url,
    echo=settings.environment == "development",
    pool_pre_ping=True,
)


def get_sync_session():
    """Get a synchronous database session for migrations."""
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=sync_engine)
    return Session()