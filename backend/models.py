"""
Pydantic models for request/response schemas.

Defines the data structures for API communication between frontend and backend.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


# Supported summary languages (must match frontend/src/types.ts SUPPORTED_LANGUAGES, alphabetical by name)
SUPPORTED_SUMMARY_LANGUAGES = ["zh", "en", "fr", "de", "ja", "ko", "pt", "es", "vi"]


class SummarizeRequest(BaseModel):
    """Request model for the summarize endpoint."""
    
    url: str = Field(
        ...,
        description="YouTube video URL to summarize",
        examples=["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]
    )
    
    # Optional parameters for future enhancements
    language: Optional[str] = Field(
        default="en",
        description="Preferred transcript language (ISO 639-1 code)",
        examples=["en", "es", "fr"]
    )
    
    summary_language: Optional[str] = Field(
        default="en",
        description="Desired language for summary output (ISO 639-1 code)",
        examples=["en", "es", "fr", "de", "vi", "zh"]
    )
    
    summary_length: Optional[str] = Field(
        default="medium",
        description="Desired summary length",
        enum=["short", "medium", "detailed"]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                "language": "en",
                "summary_length": "medium"
            }
        }


class VideoMetadata(BaseModel):
    """Metadata about a YouTube video."""
    
    video_id: str = Field(..., description="YouTube video ID")
    title: str = Field(..., description="Video title")
    channel: str = Field(..., description="Channel name")
    channel_id: Optional[str] = Field(None, description="Channel ID")
    duration: int = Field(..., description="Video duration in seconds")
    view_count: Optional[int] = Field(None, description="Number of views")
    upload_date: Optional[str] = Field(None, description="Upload date (YYYYMMDD)")
    description: Optional[str] = Field(None, description="Video description (truncated)")
    thumbnail: Optional[str] = Field(None, description="Thumbnail URL")
    categories: Optional[List[str]] = Field(default_factory=list, description="Video categories")
    tags: Optional[List[str]] = Field(default_factory=list, description="Video tags")


class TranscriptData(BaseModel):
    """Transcript data for a YouTube video."""
    
    video_id: str = Field(..., description="YouTube video ID")
    language: str = Field(..., description="Transcript language")
    language_code: str = Field(..., description="ISO language code")
    is_generated: bool = Field(..., description="Whether transcript is auto-generated")
    snippet_count: int = Field(..., description="Number of transcript snippets")
    total_duration: float = Field(..., description="Total duration covered by transcript")
    total_text: str = Field(..., description="Full transcript text")
    word_count: int = Field(..., description="Approximate word count")
    character_count: int = Field(..., description="Character count")
    token_count: Optional[int] = Field(None, description="Token count (if calculated)")
    
    # Raw transcript snippets (optional, for debugging)
    transcript: Optional[List[Dict[str, Any]]] = Field(
        None,
        description="Raw transcript snippets (text, start, duration)"
    )


class LLMStats(BaseModel):
    """Statistics about the LLM API call."""
    
    model: str = Field(..., description="LLM model used")
    provider: str = Field(..., description="LLM provider (e.g., openrouter)")
    input_tokens: int = Field(..., description="Input tokens consumed")
    output_tokens: int = Field(..., description="Output tokens generated")
    total_tokens: int = Field(..., description="Total tokens used")
    finish_reason: str = Field(..., description="Reason generation finished")
    estimated_cost_usd: str = Field(..., description="Estimated cost in USD")
    api_time: float = Field(..., description="API call duration in seconds")


class SummarizeResponse(BaseModel):
    """Response model for successful summarization."""
    
    success: bool = Field(True, description="Whether summarization succeeded")
    summary: str = Field(..., description="AI-generated summary of the video")
    video_id: str = Field(..., description="YouTube video ID")
    
    # Metadata
    metadata: VideoMetadata = Field(..., description="Video metadata")
    transcript_stats: TranscriptData = Field(..., description="Transcript statistics")
    llm_stats: LLMStats = Field(..., description="LLM API statistics")
    
    # Processing info
    processing_time: float = Field(..., description="Total processing time in seconds")
    timestamp: str = Field(..., description="ISO timestamp of processing")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "summary": "This video discusses the importance of...",
                "video_id": "dQw4w9WgXcQ",
                "metadata": {
                    "video_id": "dQw4w9WgXcQ",
                    "title": "Example Video Title",
                    "channel": "Example Channel",
                    "duration": 300,
                    "view_count": 1000000
                },
                "transcript_stats": {
                    "video_id": "dQw4w9WgXcQ",
                    "language": "English",
                    "language_code": "en",
                    "is_generated": False,
                    "snippet_count": 50,
                    "total_duration": 300.0,
                    "total_text": "Full transcript text here...",
                    "word_count": 1500,
                    "character_count": 7500
                },
                "llm_stats": {
                    "model": "deepseek/deepseek-v3.2",
                    "provider": "openrouter",
                    "input_tokens": 1200,
                    "output_tokens": 250,
                    "total_tokens": 1450,
                    "finish_reason": "stop",
                    "estimated_cost_usd": "$0.000406",
                    "api_time": 3.5
                },
                "processing_time": 8.2,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    success: bool = Field(False, description="Always false for error responses")
    error: str = Field(..., description="Error message")
    error_code: str = Field(..., description="Machine-readable error code")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": False,
                "error": "No subtitles available for this video",
                "error_code": "NO_SUBTITLES_AVAILABLE",
                "details": {
                    "video_id": "dQw4w9WgXcQ",
                    "suggested_action": "Try a different video with enabled captions"
                }
            }
        }


# Error code constants (for consistent error handling)
class ErrorCodes:
    """Standard error codes for the API."""
    
    # Input validation errors (400)
    INVALID_URL = "INVALID_URL"
    MISSING_URL = "MISSING_URL"
    
    # YouTube API errors (422)
    NO_SUBTITLES_AVAILABLE = "NO_SUBTITLES_AVAILABLE"
    TRANSCRIPTS_DISABLED = "TRANSCRIPTS_DISABLED"
    VIDEO_NOT_FOUND = "VIDEO_NOT_FOUND"
    VIDEO_PRIVATE = "VIDEO_PRIVATE"
    
    # LLM API errors (500, 502, 503)
    LLM_API_ERROR = "LLM_API_ERROR"
    LLM_RATE_LIMITED = "LLM_RATE_LIMITED"
    LLM_TIMEOUT = "LLM_TIMEOUT"
    
    # Internal errors (500)
    INTERNAL_ERROR = "INTERNAL_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"


# ============================================
# Authentication Models (TSK-0301)
# ============================================

class User(BaseModel):
    """User model for authentication."""
    
    id: Optional[int] = Field(None, description="User ID")
    email: str = Field(..., description="User email (unique)")
    username: Optional[str] = Field(None, description="Username")
    hashed_password: str = Field(..., description="Hashed password")
    created_at: Optional[str] = Field(None, description="ISO timestamp of creation")


class UserCreate(BaseModel):
    """Request model for user registration."""
    
    email: str = Field(..., description="User email", examples=["user@example.com"])
    password: str = Field(..., description="User password (min 8 chars)", min_length=8)
    username: Optional[str] = Field(None, description="Optional username")


class UserLogin(BaseModel):
    """Request model for user login."""
    
    email: str = Field(..., description="User email", examples=["user@example.com"])
    password: str = Field(..., description="User password")


class Token(BaseModel):
    """Response model for authentication token."""
    
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration in seconds")
    

class TokenData(BaseModel):
    """Token payload data (decoded from JWT)."""
    
    sub: str = Field(..., description="Subject (user email)")
    exp: int = Field(..., description="Expiration timestamp")


# ============================================
# History Models (TSK-0302)
# ============================================

class SummaryHistoryItem(BaseModel):
    """A single summary history item."""
    
    id: int = Field(..., description="History entry ID")
    video_id: str = Field(..., description="YouTube video ID")
    video_title: str = Field(..., description="Video title")
    summary: str = Field(..., description="Summary text")
    created_at: str = Field(..., description="ISO timestamp")


class HistoryList(BaseModel):
    """Response model for history list."""
    
    items: List[SummaryHistoryItem] = Field(default_factory=list, description="List of history items")
    total: int = Field(0, description="Total number of items")