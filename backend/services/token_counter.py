"""
Token counting and text truncation utilities.

This module handles:
- Token counting using tiktoken
- Safe text truncation to fit token limits
- Model-specific encoding handling
"""

import tiktoken
from typing import Dict, Any, Optional

from ..config import settings


def count_tokens(text: str, model: Optional[str] = None) -> int:
    """
    Count tokens in text using tiktoken.
    
    Args:
        text: Text to count tokens for
        model: Model name (default: from settings.llm_model)
        
    Returns:
        Number of tokens
    """
    if model is None:
        model = settings.llm_model
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base encoding (used by GPT-4 and DeepSeek)
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def truncate_text_to_tokens(
    text: str, 
    max_tokens: int, 
    model: Optional[str] = None,
    add_ellipsis: bool = True
) -> str:
    """
    Safely truncate text to fit within token limit.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens allowed
        model: Model name for encoding
        add_ellipsis: Whether to add "..." at the end
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if model is None:
        model = settings.llm_model
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    if add_ellipsis:
        # Reserve 3 tokens for "..."
        truncated_tokens = tokens[:max_tokens - 3]
        truncated_text = encoding.decode(truncated_tokens) + "..."
    else:
        truncated_tokens = tokens[:max_tokens]
        truncated_text = encoding.decode(truncated_tokens)
    
    return truncated_text


def estimate_tokens_for_summarization(
    transcript_text: str,
    metadata: Dict[str, Any],
    system_prompt: str,
    user_prompt_template: str
) -> Dict[str, Any]:
    """
    Estimate token counts for a summarization request.
    
    Args:
        transcript_text: Transcript text
        metadata: Video metadata
        system_prompt: System prompt text
        user_prompt_template: User prompt template with placeholders
        
    Returns:
        Dictionary with token estimates
    """
    # Fill in the user prompt template
    user_prompt = user_prompt_template.format(
        title=metadata.get('title', 'Unknown'),
        channel=metadata.get('channel', 'Unknown'),
        duration=metadata.get('duration', 0),
        transcript=transcript_text
    )
    
    # Count tokens
    transcript_tokens = count_tokens(transcript_text)
    system_tokens = count_tokens(system_prompt)
    user_tokens = count_tokens(user_prompt)
    
    total_tokens = transcript_tokens + system_tokens + user_tokens
    
    return {
        'transcript_tokens': transcript_tokens,
        'system_tokens': system_tokens,
        'user_tokens': user_tokens,
        'total_tokens': total_tokens,
        'needs_truncation': total_tokens > settings.max_input_tokens,
        'available_tokens': settings.max_input_tokens - (system_tokens + user_tokens)
    }


def get_encoding_for_model(model: Optional[str] = None) -> tiktoken.Encoding:
    """
    Get tiktoken encoding for a model.
    
    Args:
        model: Model name (default: from settings.llm_model)
        
    Returns:
        tiktoken.Encoding object
    """
    if model is None:
        model = settings.llm_model
    
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")