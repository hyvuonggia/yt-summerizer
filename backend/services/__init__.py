"""
Service modules for the YouTube Video Summarizer backend.

This package contains the business logic for:
- Transcript fetching and validation
- Video metadata extraction
- LLM summarization
- Token counting and text processing
"""

from .transcript import extract_video_id, fetch_transcript, validate_youtube_url
from .metadata import fetch_video_metadata, get_basic_metadata
from .token_counter import count_tokens, truncate_text_to_tokens, get_encoding_for_model
from .summarization import (
    initialize_openrouter_client,
    create_summarization_prompt,
    call_llm_summarize,
    format_time
)

__all__ = [
    # Transcript
    'extract_video_id',
    'fetch_transcript',
    'validate_youtube_url',
    
    # Metadata
    'fetch_video_metadata',
    'get_basic_metadata',
    
    # Token counter
    'count_tokens',
    'truncate_text_to_tokens',
    'get_encoding_for_model',
    
    # Summarization
    'initialize_openrouter_client',
    'create_summarization_prompt',
    'call_llm_summarize',
    'format_time',
]