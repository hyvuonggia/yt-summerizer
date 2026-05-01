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
# In-Memory User Storage (TSK-0301)
# ============================================

class InMemoryUserStore:
    """
    In-memory user storage.
    
    Note: This is for development/demo purposes. 
    Database-backed storage will be implemented in P3.2.
    """
    
    def __init__(self):
        self._users: Dict[str, Dict[str, Any]] = {}  # email -> user data
        self._id_counter: int = 1
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email."""
        return self._users.get(email.lower())
    
    def create_user(self, email: str, username: Optional[str], hashed_password: str) -> Dict[str, Any]:
        """Create a new user."""
        user_id = self._id_counter
        self._id_counter += 1
        
        user = {
            "id": user_id,
            "email": email.lower(),
            "username": username or email.split("@")[0],
            "hashed_password": hashed_password,
            "created_at": utcnow().isoformat()
        }
        
        self._users[email.lower()] = user
        auth_logger.info(f"User created: {email.lower()}")
        
        return user
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists."""
        return email.lower() in self._users


# Global user store instance
user_store = InMemoryUserStore()


# ============================================
# In-Memory Summary/History Storage
# ============================================

class InMemoryHistoryStore:
    """In-memory history storage for summarized videos."""
    
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


# Global history store instance
history_store = InMemoryHistoryStore()


# ============================================
# Auth Service Functions
# ============================================
# Auth Service Functions
# ============================================
# In-Memory Summary/History Storage (TSK-0302)
# ============================================

class InMemoryHistoryStore:
    """
    In-memory history storage for summarized videos.
    
    Note: This is for development/demo purposes.
    Database-backed storage will be implemented in P3.2.
    """
    
    def __init__(self):
        self._histories: Dict[int, List[Dict[str, Any]]] = {}  # user_id -> list of summaries
    
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
        return histories[-limit:][::-1]  # Most recent first
    
    def delete_summary(self, user_id: int, summary_id: int) -> bool:
        """Delete a summary from user's history."""
        if user_id not in self._histories:
            return False
        
        self._histories[user_id] = [h for h in self._histories[user_id] if h["id"] != summary_id]
        return True


# Global history store instance
history_store = InMemoryHistoryStore()


# ============================================
# Auth Service Functions
# ============================================

def register_user(email: str, password: str, username: Optional[str] = None) -> Dict[str, Any]:
    """
    Register a new user.
    
    Args:
        email: User email
        password: User password
        username: Optional username
        
    Returns:
        Created user data (without password)
        
    Raises:
        ValueError: If user already exists
    """
    email = email.lower().strip()
    
    if user_store.user_exists(email):
        raise ValueError(f"User already exists: {email}")
    
    hashed_pwd = hash_password(password)
    user = user_store.create_user(email, username, hashed_pwd)
    
    # Return user without password
    return {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"],
        "created_at": user["created_at"]
    }


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        User data if authenticated, None otherwise
    """
    email = email.lower().strip()
    
    user = user_store.get_user_by_email(email)
    if not user:
        return None
    
    if not verify_password(password, user["hashed_password"]):
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