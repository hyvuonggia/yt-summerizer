"""
LLM summarization service.

This module handles:
- LLM API calls via OpenRouter
- Prompt engineering for YouTube summarization
- Error handling and retry logic
- Cost estimation
- Progress reporting during long-running operations
"""

import os
import time
import threading
import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from openai import OpenAI
from openai.types.chat import ChatCompletion

from ..config import settings
from .token_counter import count_tokens, truncate_text_to_tokens

# Configure logger for this module
logger = logging.getLogger("backend.summarization")


def initialize_openrouter_client() -> OpenAI:
    """
    Initialize OpenAI client for OpenRouter.
    
    Returns:
        OpenAI client configured for OpenRouter
        
    Raises:
        ValueError: If API key is missing
    """
    # Get API key from environment
    api_key = settings.openrouter_api_key
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please check your .env file.")
    
    # Initialize client with OpenRouter configuration
    client = OpenAI(
        base_url=settings.openrouter_base_url,
        api_key=api_key,
        timeout=30.0,
    )
    
    return client


def create_summarization_prompt(
    transcript_text: str, 
    metadata: Dict[str, Any],
    summary_language: str = "en"
) -> List[Dict[str, str]]:
    """
    Create system and user prompts for YouTube summarization.
    
    Args:
        transcript_text: Full transcript text
        metadata: Video metadata
        summary_language: Language for the summary output (ISO 639-1 code)
        
    Returns:
        List of message dictionaries for OpenAI API
    """
    # Map language codes to display names
    language_names = {
        "en": "English", "es": "Spanish", "fr": "French", "de": "German",
        "it": "Italian", "pt": "Portuguese", "ru": "Russian", "zh": "Chinese",
        "ja": "Japanese", "ko": "Korean", "vi": "Vietnamese", "ar": "Arabic",
        "hi": "Hindi", "nl": "Dutch", "pl": "Polish", "tr": "Turkish"
    }
    lang_name = language_names.get(summary_language, summary_language.upper())
    
    # System prompt for YouTube summarization
    system_prompt = f"""You are an expert YouTube video summarizer. Your task is to create concise, informative summaries of video transcripts.

Follow these guidelines:
1. Extract the main topic and purpose of the video
2. Identify 3-5 key points or takeaways
3. Note any important examples, data, or quotes
4. Summarize the conclusion or call to action
5. Keep the summary under 300 words
6. Use clear, accessible language
7. Maintain a neutral, informative tone
8. ALWAYS write the summary in {lang_name}

Format your response as:
**Main Topic**: [1-2 sentence summary]
**Key Points**:
- [Point 1]
- [Point 2]
- [Point 3]
**Conclusion**: [1-2 sentence conclusion]

Do not add commentary or opinions. Stick to facts presented in the transcript."""
    
    # User prompt with context
    user_prompt = f"""Please summarize this YouTube video transcript:

Video Title: {metadata.get('title', 'Unknown')}
Channel: {metadata.get('channel', 'Unknown')}
Video Duration: {metadata.get('duration', 0)} seconds

Transcript:
{transcript_text}

Please provide a concise summary following the format specified above."""
    
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]


def _create_progress_counter(prefix: str = "Waiting"):
    """Create a live progress counter for long-running operations."""
    counter = [0]
    running = [True]
    
    def counter_thread():
        while running[0]:
            time.sleep(1)
            counter[0] += 1
            print(f"   {prefix}... ({counter[0]}s)", end="\r", flush=True)
    
    thread = threading.Thread(target=counter_thread, daemon=True)
    thread.start()
    
    return counter, running, thread


def call_llm_summarize(
    transcript_text: str,
    metadata: Dict[str, Any],
    max_input_tokens: Optional[int] = None,
    max_output_tokens: Optional[int] = None,
    summary_language: str = "en"
) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Call LLM to summarize transcript using OpenRouter.
    
    Args:
        transcript_text: Transcript text to summarize
        metadata: Video metadata
        max_input_tokens: Maximum input tokens (default: from settings)
        max_output_tokens: Maximum output tokens (default: from settings)
        summary_language: Language for summary output (ISO 639-1 code)
        
    Returns:
        Tuple of (summary_text, stats_dict)
    """
    # Use settings defaults if not provided
    if max_input_tokens is None:
        max_input_tokens = settings.max_input_tokens
    if max_output_tokens is None:
        max_output_tokens = settings.max_output_tokens
    
    # Initialize client
    try:
        client = initialize_openrouter_client()
    except ValueError as e:
        return None, {"error": str(e), "error_code": "CONFIGURATION_ERROR"}
    
    # Count tokens in transcript
    transcript_tokens = count_tokens(transcript_text)
    
    # Check if transcript needs truncation
    # Reserve tokens for prompts and metadata (estimate ~500 tokens)
    available_tokens = max_input_tokens - 500
    if transcript_tokens > available_tokens:
        logger.info(f"Transcript exceeds token limit ({transcript_tokens:,} > {available_tokens:,})")
        logger.info(f"Truncating transcript to {available_tokens:,} tokens")
        transcript_text = truncate_text_to_tokens(transcript_text, available_tokens)
        transcript_tokens = count_tokens(transcript_text)
        logger.info(f"Transcript truncated to {transcript_tokens:,} tokens")
    
    # Create prompts
    messages = create_summarization_prompt(transcript_text, metadata, summary_language)
    
    # Count total tokens for the request
    prompt_tokens = sum(count_tokens(msg["content"]) for msg in messages)
    total_tokens_estimate = transcript_tokens + prompt_tokens
    
    # Call LLM with retry logic
    max_retries = 3
    retry_delay = 2  # seconds
    
    for attempt in range(max_retries):
        try:
            model_display = settings.llm_model.split('/')[-1]  # Show just the model name
            
            # Live counter for API call
            counter, running, thread = _create_progress_counter("Waiting for LLM response")
            
            api_start = time.time()
            response = client.chat.completions.create(
                model=settings.llm_model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent summaries
                max_tokens=max_output_tokens,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
            )
            api_time = time.time() - api_start
            
            # Stop counter
            running[0] = False
            thread.join(timeout=0.1)
            
            # Extract summary
            summary = response.choices[0].message.content
            
            # Log progress
            logger.info(f"LLM response received - {response.usage.total_tokens:,} total tokens, "
                        f"{response.usage.completion_tokens:,} output tokens")
            
            # Calculate estimated cost (approximate)
            # DeepSeek v3.2 pricing: $0.14 per 1M input tokens, $0.28 per 1M output tokens
            input_cost = (response.usage.prompt_tokens * 0.14 / 1_000_000)
            output_cost = (response.usage.completion_tokens * 0.28 / 1_000_000)
            total_cost = input_cost + output_cost
            
            # Collect stats
            stats = {
                "success": True,
                "model": response.model,
                "provider": settings.llm_provider,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason,
                "estimated_cost_usd": f"${total_cost:.6f}",
                "transcript_tokens": transcript_tokens,
                "prompt_tokens": prompt_tokens,
                "api_time": api_time,
                "timestamp": datetime.now().isoformat(),
            }
            
            return summary, stats
            
        except Exception as e:
            error_type = type(e).__name__
            
            # Check if it's a retryable error
            is_retryable = False
            retryable_errors = ['RateLimitError', 'APITimeoutError', 'APIConnectionError', 
                               'ConnectionError', 'TimeoutError', 'InternalServerError']
            
            for retryable_error in retryable_errors:
                if retryable_error in error_type or retryable_error in str(e):
                    is_retryable = True
                    break
            
            if is_retryable and attempt < max_retries - 1:
                logger.warning(f"Retryable error: {error_type}: {e}")
                logger.info(f"Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                error_code = "LLM_RATE_LIMITED" if "RateLimit" in error_type else "LLM_API_ERROR"
                return None, {
                    "error": f"{error_type}: {str(e)}",
                    "error_code": error_code,
                    "attempts": attempt + 1
                }
    
    return None, {"error": "Max retries exceeded", "error_code": "LLM_TIMEOUT"}


def format_time(seconds: float) -> str:
    """Format time in a human-readable way."""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"