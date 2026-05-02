"""
Authentication service for user management and JWT token handling.

Provides:
- User registration and login
- JWT token generation and validation
- Password hashing (bcrypt)

Dependencies:
- python-jose[cryptography] for JWT
- bcrypt for password hashing
"""

from __future__ import annotations

import os
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any, List
from functools import wraps

# Security imports
import bcrypt
from jose import JWTError, jwt

# Configure logging
auth_logger = logging.getLogger("backend.auth")

# Current time as UTC (timezone-aware)
def utcnow() -> datetime:
    """Get current UTC time as timezone-aware datetime."""
    return datetime.now(timezone.utc)

# ============================================
# Configuration
# ============================================

# JWT settings
JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


# ============================================
# Password Utilities
# ============================================

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    # Truncate to 72 bytes (bcrypt limit)
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hash to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        # Truncate to 72 bytes (bcrypt limit)
        password_bytes = plain_password.encode('utf-8')[:72]
        hashed_bytes = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        auth_logger.warning(f"Password verification error: {e}")
        return False


# ============================================
# JWT Token Functions
# ============================================

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Payload data to encode
        expires_delta: Optional expiration time delta
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = utcnow() + expires_delta
    else:
        expire = utcnow() + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Store as Unix timestamp integer (required by jose)
    to_encode.update({"exp": int(expire.timestamp())})
    
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token (without automatic expiration validation).
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded token payload or None if invalid
    """
    try:
        # Decode without automatic expiration check - we'll do our own
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM], options={"verify_exp": False})
        return payload
    except JWTError as e:
        auth_logger.warning(f"JWT decode error: {e}")
        return None


def get_token_expiration(token: str) -> Optional[int]:
    """
    Get the expiration timestamp from a token.
    
    Args:
        token: JWT token string
        
    Returns:
        Expiration timestamp or None if invalid
    """
    payload = decode_token(token)
    if payload is None:
        return None
    
    exp = payload.get("exp")
    if exp is None:
        return None
    
    # Handle both datetime objects and numeric timestamps
    if isinstance(exp, datetime):
        return int(exp.timestamp())
    return int(exp)


def is_token_expired(token: str) -> bool:
    """
    Check if a token is expired.
    
    Args:
        token: JWT token string
        
    Returns:
        True if expired or invalid, False otherwise
    """
    exp = get_token_expiration(token)
    if exp is None:
        return True
    
    # Compare with current time
    return utcnow().timestamp() > exp


# ============================================
# Database-Backed User Storage (Sprint P3.2)
# ============================================

class DatabaseUserStore:
    """
    Database-backed user storage.
    
    Uses MySQL database for persistent storage.
    Password hashing is handled by bcrypt (hash_password function above).
    """
    
    async def get_user_by_email(self, email: str, db) -> Optional[Dict[str, Any]]:
        """Get user by email from database."""
        from sqlalchemy import select
        from ..database import User
        
        result = await db.execute(
            select(User).where(User.email == email.lower())
        )
        user = result.scalar_one_or_none()
        
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "password": user.password,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
        return None
    
    async def create_user(self, email: str, username: Optional[str], hashed_password: str, db) -> Dict[str, Any]:
        """Create a new user in database."""
        from ..database import User
        
        user = User(
            email=email.lower(),
            username=username or email.split("@")[0],
            password=hashed_password
        )
        
        db.add(user)
        await db.commit()
        await db.refresh(user)
        
        auth_logger.info(f"User created in database: {email.lower()}")
        
        return {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "password": user.password,
            "created_at": user.created_at.isoformat() if user.created_at else None
        }
    
    async def user_exists(self, email: str, db) -> bool:
        """Check if user exists in database."""
        from sqlalchemy import select, func
        from ..database import User
        
        result = await db.execute(
            select(func.count(User.id)).where(User.email == email.lower())
        )
        count = result.scalar()
        return count > 0


# Global user store instance
user_store = DatabaseUserStore()


# ============================================
# Legacy In-Memory User Storage (for fallback)
# ============================================
# Database-Backed History Storage (Sprint P3.2)
# ============================================

class DatabaseHistoryStore:
    """
    Database-backed history storage.
    
    Persists summaries to MySQL database.
    """
    
    async def add_summary(
        self,
        user_id: int,
        video_id: str,
        video_title: str,
        summary: str,
        db,
        video_url: Optional[str] = None,
        video_channel: Optional[str] = None,
        transcript_language: Optional[str] = None,
        transcript_word_count: Optional[int] = None,
        transcript_duration: Optional[int] = None,
        llm_provider: Optional[str] = None,
        llm_model: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Add a summary to user's history in database."""
        from ..database import Summary
        
        summary_obj = Summary(
            user_id=user_id,
            video_id=video_id,
            video_title=video_title,
            video_url=video_url,
            video_channel=video_channel,
            transcript_language=transcript_language,
            transcript_word_count=transcript_word_count,
            transcript_duration=transcript_duration,
            llm_provider=llm_provider,
            llm_model=llm_model,
            summary_text=summary
        )
        
        db.add(summary_obj)
        await db.commit()
        await db.refresh(summary_obj)
        
        auth_logger.info(f"Summary saved to database for user {user_id}: video {video_id}")
        
        return {
            "id": summary_obj.id,
            "video_id": summary_obj.video_id,
            "video_title": summary_obj.video_title,
            "summary": summary_obj.summary_text,
            "created_at": summary_obj.created_at.isoformat() if summary_obj.created_at else None
        }
    
    async def get_user_history(self, user_id: int, limit: int = 50, db=None) -> List[Dict[str, Any]]:
        """Get user's summary history from database."""
        from sqlalchemy import select, desc
        from ..database import Summary
        
        result = await db.execute(
            select(Summary)
            .where(Summary.user_id == user_id)
            .order_by(desc(Summary.created_at))
            .limit(limit)
        )
        summaries = result.scalars().all()
        
        return [
            {
                "id": s.id,
                "video_id": s.video_id,
                "video_title": s.video_title,
                "summary": s.summary_text,
                "created_at": s.created_at.isoformat() if s.created_at else None
            }
            for s in summaries
        ]
    
    async def delete_summary(self, user_id: int, summary_id: int, db) -> bool:
        """Delete a summary from user's history in database."""
        from sqlalchemy import select, delete
        from ..database import Summary
        
        # First check if the summary belongs to the user
        result = await db.execute(
            select(Summary).where(
                Summary.id == summary_id,
                Summary.user_id == user_id
            )
        )
        summary = result.scalar_one_or_none()
        
        if not summary:
            return False
        
        await db.delete(summary)
        await db.commit()
        
        auth_logger.info(f"Summary {summary_id} deleted from database by user {user_id}")
        return True


# Global history store instance
history_store = DatabaseHistoryStore()


# ============================================
# Legacy In-Memory History Storage (fallback)
# ============================================

class InMemoryHistoryStore:
    """In-memory history storage (fallback when DB unavailable)."""
    
    def __init__(self):
        self._histories: dict[int, list[dict[str, Any]]] = {}
    
    def add_summary(self, user_id: int, video_id: str, video_title: str, summary: str) -> Dict[str, Any]:
        """Add a summary to user's history."""
        if user_id not in self._histories:
            self._histories[user_id] = []
        
        entry = {
            "id": len(self._histories[user_id]) + 1,
            "video_id": video_id,
            "video_title": video_title,
            "summary": summary,
            "created_at": utcnow().isoformat()
        }
        
        self._histories[user_id].append(entry)
        return entry
    
    def get_user_history(self, user_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get user's summary history."""
        histories = self._histories.get(user_id, [])
        return histories[-limit:][::-1]
    
    def delete_summary(self, user_id: int, summary_id: int) -> bool:
        """Delete a summary from user's history."""
        if user_id not in self._histories:
            return False
        
        self._histories[user_id] = [h for h in self._histories[user_id] if h["id"] != summary_id]
        return True


# Fallback history store
_fallback_history_store = InMemoryHistoryStore()


# ============================================
# Auth Service Functions (Database-backed)
# ============================================

async def register_user(email: str, password: str, username: Optional[str] = None, db=None) -> Dict[str, Any]:
    """
    Register a new user.
    
    Args:
        email: User email
        password: User password
        username: Optional username
        db: Database session
        
    Returns:
        Created user data (without password)
        
    Raises:
        ValueError: If user already exists
    """
    email = email.lower().strip()
    
    if await user_store.user_exists(email, db):
        raise ValueError(f"User already exists: {email}")
    
    # Hash password using bcrypt (industry standard)
    hashed_pwd = hash_password(password)
    user = await user_store.create_user(email, username, hashed_pwd, db)
    
    # Return user without password
    return {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "created_at": user["created_at"]
    }


async def authenticate_user(email: str, password: str, db=None) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user.
    
    Args:
        email: User email
        password: User password
        db: Database session
        
    Returns:
        User data if authenticated, None otherwise
    """
    email = email.lower().strip()
    
    user = await user_store.get_user_by_email(email, db)
    if not user:
        return None
    
    # Verify password against bcrypt hash
    if not verify_password(password, user["password"]):
        return None
    
    return user


def create_token_for_user(email: str, user_id: int) -> str:
    """
    Create a JWT token for an authenticated user.
    
    Args:
        email: User email
        user_id: User ID
        
    Returns:
        JWT token string
    """
    token_data = {
        "sub": email,
        "user_id": user_id
    }
    
    return create_access_token(
        token_data,
        timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def generate_token_response(email: str, user_id: int) -> Dict[str, Any]:
    """
    Generate a complete token response.
    
    Args:
        email: User email
        user_id: User ID
        
    Returns:
        Token response with access_token, token_type, expires_in
    """
    access_token = create_token_for_user(email, user_id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }