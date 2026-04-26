#!/usr/bin/env python3
"""
YouTube Video Summarizer - Proof of Concept (Sprint P1.2)

This script implements end-to-end YouTube video summarization:
1. Extracts video ID from URL
2. Fetches transcript using youtube-transcript-api
3. Retrieves metadata using yt-dlp
4. Calls LLM (DeepSeek v3.2 via OpenRouter) for summarization
5. Implements token-aware truncation using tiktoken
6. Handles error cases with clear messages

Usage:
    python poc_summarize.py <YOUTUBE_URL>

Example:
    python poc_summarize.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

Requirements:
    - OpenRouter API key in .env file (OPENROUTER_API_KEY)
    - Python dependencies: youtube-transcript-api, yt-dlp, tiktoken, python-dotenv, openai
"""

import sys
import re
import os
import time
from typing import Optional, Dict, Any, List, Tuple
from urllib.parse import urlparse, parse_qs

# Third-party imports
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    import yt_dlp
except Exception as e:
    print(f"Error during import: {e}")
    print("Please check dependencies: pip install youtube-transcript-api yt-dlp")
    import traceback
    traceback.print_exc()
    sys.exit(1)


def extract_video_id(url: str) -> Optional[str]:
    """
    Extract YouTube video ID from various URL formats.
    
    Supported formats:
    - Standard: https://www.youtube.com/watch?v=VIDEO_ID
    - Short: https://youtu.be/VIDEO_ID
    - Embedded: https://www.youtube.com/embed/VIDEO_ID
    - Mobile: https://m.youtube.com/watch?v=VIDEO_ID
    
    Args:
        url: YouTube video URL
        
    Returns:
        Video ID string or None if extraction fails
    """
    # Common YouTube URL patterns
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    # Try parsing query parameters
    parsed = urlparse(url)
    if parsed.netloc in ['www.youtube.com', 'youtube.com', 'm.youtube.com']:
        query_params = parse_qs(parsed.query)
        if 'v' in query_params:
            return query_params['v'][0]
    
    return None


def fetch_transcript(video_id: str) -> Dict[str, Any]:
    """
    Fetch transcript for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with transcript data or error information
        
    Raises:
        TranscriptsDisabled: When transcripts are disabled for the video
        NoTranscriptFound: When no transcript is available
        Exception: For other errors (network, permission, etc.)
    """
    import threading
    
    # Live counter for progress
    counter = [0]
    running = [True]
    
    def counter_thread():
        while running[0]:
            time.sleep(1)
            counter[0] += 1
            print(f"   Fetching transcript... ({counter[0]}s)", end="\r", flush=True)
    
    thread = threading.Thread(target=counter_thread, daemon=True)
    thread.start()
    
    try:
        # Create API instance
        ytt_api = YouTubeTranscriptApi()
        
        # Try to fetch English transcript first
        try:
            # First try to list transcripts to get metadata
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript(['en'])
            fetched_transcript = transcript.fetch()
            
            # Extract metadata from transcript object
            language = transcript.language
            language_code = transcript.language_code
            is_generated = transcript.is_generated
            
            # Convert FetchedTranscript to list of dictionaries
            snippets = []
            for snippet in fetched_transcript:
                snippets.append({
                    'text': snippet.text,
                    'start': snippet.start,
                    'duration': snippet.duration
                })
                
        except Exception as list_error:
            # Fallback: try direct fetch (might not have metadata)
            print(f"   Note: Using direct fetch (metadata may be limited): {list_error}")
            fetched_transcript = ytt_api.fetch(video_id, languages=['en'])
            
            # Convert to list of dictionaries
            snippets_list = []
            for snippet in fetched_transcript:
                snippets_list.append({
                    'text': snippet.text,
                    'start': snippet.start,
                    'duration': snippet.duration
                })
            snippets = snippets_list
            language = "English"
            language_code = "en"
            is_generated = False
        
        # Validate we have transcript data
        if not snippets:
            raise NoTranscriptFound(f"Transcript fetched but empty for video {video_id}")
        
        # Calculate totals
        transcript_data = []
        total_duration = 0
        text_parts = []
        
        for snippet in snippets:
            transcript_data.append(snippet)
            total_duration += snippet['duration']
            text_parts.append(snippet['text'])
        
        total_text = " ".join(text_parts)
        
        running[0] = False
        thread.join(timeout=0.1)
        print(f"   Fetching transcript... ({counter[0]}s) - Done")
        print("   ", end="")  # Indent for next output
        
        return {
            'success': True,
            'video_id': video_id,
            'language': language,
            'language_code': language_code,
            'is_generated': is_generated,
            'snippet_count': len(transcript_data),
            'total_duration': total_duration,
            'total_text': total_text.strip(),
            'transcript': transcript_data
        }
        
    except TranscriptsDisabled as e:
        running[0] = False
        raise TranscriptsDisabled(f"Transcripts are disabled for video {video_id}") from e
    except NoTranscriptFound as e:
        running[0] = False
        raise NoTranscriptFound(f"No transcript found for video {video_id}") from e
    except Exception as e:
        running[0] = False
        raise Exception(f"Error fetching transcript: {str(e)}") from e
    except Exception as e:
        raise Exception(f"Error fetching transcript: {str(e)}") from e


def fetch_video_metadata(video_id: str) -> Dict[str, Any]:
    """
    Fetch video metadata (title, channel) using yt-dlp info-only mode.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with video metadata
        
    Raises:
        Exception: If metadata extraction fails
    """
    import threading
    
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': False,
    }
    
    # Live counter for progress
    counter = [0]
    running = [True]
    
    def counter_thread():
        while running[0]:
            time.sleep(1)
            counter[0] += 1
            print(f"   Fetching... ({counter[0]}s)", end="\r", flush=True)
    
    thread = threading.Thread(target=counter_thread, daemon=True)
    thread.start()
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        running[0] = False
        thread.join(timeout=0.1)
        print(f"   Fetching... ({counter[0]}s) - Done")
        print("   ", end="")  # Indent for next output
        
        return {
            'success': True,
            'video_id': video_id,
            'title': info.get('title', 'Unknown'),
            'channel': info.get('uploader', 'Unknown'),
            'channel_id': info.get('uploader_id', 'Unknown'),
            'duration': info.get('duration', 0),
            'view_count': info.get('view_count', 0),
            'upload_date': info.get('upload_date', 'Unknown'),
            'description': info.get('description', '')[:200] + '...' if info.get('description') else '',
            'thumbnail': info.get('thumbnail', ''),
            'categories': info.get('categories', []),
            'tags': info.get('tags', [])[:5]  # First 5 tags only
        }
        
    except yt_dlp.utils.DownloadError as e:
        running[0] = False
        raise Exception(f"Invalid URL or video not found: {str(e)}")
    except Exception as e:
        running[0] = False
        raise Exception(f"Error fetching metadata: {str(e)}")


def count_tokens(text: str, model: str = "gpt-4") -> int:
    """
    Count tokens in text using tiktoken.
    
    Args:
        text: Text to count tokens for
        model: Model name (default: "gpt-4" which uses cl100k_base encoding)
        
    Returns:
        Number of tokens
    """
    try:
        import tiktoken
    except ImportError:
        print("Error: tiktoken not installed. Please install with: pip install tiktoken")
        return len(text) // 4  # Rough estimate
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        # Fallback to cl100k_base encoding (used by GPT-4 and DeepSeek)
        encoding = tiktoken.get_encoding("cl100k_base")
    
    return len(encoding.encode(text))


def truncate_text_to_tokens(text: str, max_tokens: int, model: str = "gpt-4") -> str:
    """
    Safely truncate text to fit within token limit.
    
    Args:
        text: Text to truncate
        max_tokens: Maximum number of tokens allowed
        model: Model name for encoding
        
    Returns:
        Truncated text with ellipsis if needed
    """
    try:
        import tiktoken
    except ImportError:
        print("Error: tiktoken not installed. Please install with: pip install tiktoken")
        # Simple character-based truncation as fallback
        if len(text) > max_tokens * 4:
            return text[:max_tokens * 4 - 3] + "..."
        return text
    
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    
    tokens = encoding.encode(text)
    
    if len(tokens) <= max_tokens:
        return text
    
    # Truncate and add ellipsis (reserve 3 tokens for "...")
    truncated_tokens = tokens[:max_tokens - 3]
    truncated_text = encoding.decode(truncated_tokens) + "..."
    
    return truncated_text


def create_summarization_prompt(transcript_text: str, metadata: Dict[str, Any]) -> List[Dict[str, str]]:
    """
    Create system and user prompts for YouTube summarization.
    
    Args:
        transcript_text: Full transcript text
        metadata: Video metadata
        
    Returns:
        List of message dictionaries for OpenAI API
    """
    # System prompt for YouTube summarization
    system_prompt = """You are an expert YouTube video summarizer. Your task is to create concise, informative summaries of video transcripts.

Follow these guidelines:
1. Extract the main topic and purpose of the video
2. Identify 3-5 key points or takeaways
3. Note any important examples, data, or quotes
4. Summarize the conclusion or call to action
5. Keep the summary under 300 words
6. Use clear, accessible language
7. Maintain a neutral, informative tone

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


def get_llm_model() -> str:
    """
    Get the LLM model from environment variables.
    
    Returns:
        Model name from LLM_MODEL env var, or default "deepseek/deepseek-v3.2"
    """
    from dotenv import load_dotenv
    load_dotenv()
    
    model = os.getenv("LLM_MODEL", "deepseek/deepseek-v3.2")
    return model


def initialize_openrouter_client():
    """
    Initialize OpenAI client for OpenRouter.
    
    Returns:
        OpenAI client configured for OpenRouter
    """
    try:
        from openai import OpenAI
        from dotenv import load_dotenv
    except ImportError as e:
        raise ImportError(f"Required package not installed: {e}. Please install with: pip install openai python-dotenv")
    
    # Load environment variables
    load_dotenv()
    
    # Get API key from environment
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY not found in environment variables. Please check your .env file.")
    
    # Initialize client with OpenRouter configuration
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    return client


def call_llm_summarize(
    transcript_text: str,
    metadata: Dict[str, Any],
    max_input_tokens: int = 120000,  # DeepSeek v3.2 has 128K context
    max_output_tokens: int = 500
) -> Tuple[Optional[str], Dict[str, Any]]:
    """
    Call LLM to summarize transcript using OpenRouter with DeepSeek v3.2.
    
    Args:
        transcript_text: Transcript text to summarize
        metadata: Video metadata
        max_input_tokens: Maximum input tokens (default: 120K for DeepSeek v3.2)
        max_output_tokens: Maximum output tokens
        
    Returns:
        Tuple of (summary_text, stats_dict)
    """
    # Initialize client
    try:
        client = initialize_openrouter_client()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return None, {"error": str(e)}
    
    # Count tokens in transcript
    transcript_tokens = count_tokens(transcript_text)
    print(f"   • Transcript tokens: {transcript_tokens:,}")
    
    # Check if transcript needs truncation
    # Reserve tokens for prompts and metadata (estimate ~500 tokens)
    available_tokens = max_input_tokens - 500
    if transcript_tokens > available_tokens:
        print(f"   ⚠️  Transcript exceeds token limit ({transcript_tokens:,} > {available_tokens:,})")
        print(f"   • Truncating transcript to {available_tokens:,} tokens...")
        transcript_text = truncate_text_to_tokens(transcript_text, available_tokens)
        transcript_tokens = count_tokens(transcript_text)
        print(f"   • Truncated to {transcript_tokens:,} tokens")
    
    # Create prompts
    messages = create_summarization_prompt(transcript_text, metadata)
    
    # Count total tokens for the request
    prompt_tokens = sum(count_tokens(msg["content"]) for msg in messages)
    total_tokens = transcript_tokens + prompt_tokens
    print(f"   • Total request tokens: {total_tokens:,}")
    
    # Call LLM with retry logic
    max_retries = 3
    retry_delay = 2  # seconds
    
    # Get model from environment (default: deepseek/deepseek-v3.2)
    model = get_llm_model()
    model_display = model.split('/')[-1]  # Show just the model name
    
    for attempt in range(max_retries):
        try:
            print(f"   • Calling {model_display} via OpenRouter (attempt {attempt + 1}/{max_retries})...")
            
            # Live counter for API call
            import threading
            counter = [0]
            running = [True]
            
            def counter_thread():
                while running[0]:
                    time.sleep(1)
                    counter[0] += 1
                    print(f"   Waiting for response... ({counter[0]}s)", end="\r", flush=True)
            
            thread = threading.Thread(target=counter_thread, daemon=True)
            thread.start()
            
            api_start = time.time()
            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=0.3,  # Lower temperature for more consistent summaries
                max_tokens=max_output_tokens,
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                timeout=30.0,  # 30 second timeout
            )
            api_time = time.time() - api_start
            
            # Stop counter
            running[0] = False
            thread.join(timeout=0.1)
            print(f"   Waiting for response... ({counter[0]}s) - Done")
            print("   ", end="")  # Indent for next output
            
            # Extract summary
            summary = response.choices[0].message.content
            
            # Collect stats
            stats = {
                "success": True,
                "model": response.model,
                "input_tokens": response.usage.prompt_tokens,
                "output_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens,
                "finish_reason": response.choices[0].finish_reason,
                "estimated_cost_usd": f"${(response.usage.prompt_tokens * 0.14 / 1_000_000) + (response.usage.completion_tokens * 0.28 / 1_000_000):.6f}",
                "transcript_tokens": transcript_tokens,
                "prompt_tokens": prompt_tokens,
                "api_time": api_time,
            }
            
            print(f"   ✓ LLM call successful ({format_time(api_time)})")
            print(f"   • Model: {stats['model']}")
            print(f"   • Tokens used: {stats['total_tokens']:,} (in: {stats['input_tokens']:,}, out: {stats['output_tokens']:,})")
            print(f"   • Estimated cost: {stats['estimated_cost_usd']}")
            
            return summary, stats
            
        except Exception as e:
            error_type = type(e).__name__
            print(f"   ⚠️  {error_type}: {e}")
            
            # Check if it's a retryable error
            is_retryable = False
            retryable_errors = ['RateLimitError', 'APITimeoutError', 'APIConnectionError', 'ConnectionError', 'TimeoutError']
            
            for retryable_error in retryable_errors:
                if retryable_error in error_type or retryable_error in str(e):
                    is_retryable = True
                    break
            
            if is_retryable and attempt < max_retries - 1:
                print(f"   • Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                print(f"   ❌ {'Max retries exceeded' if is_retryable else 'Non-retryable error'}")
                return None, {"error": f"{error_type}: {str(e)}"}
            
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")
            return None, {"error": f"Unexpected error: {str(e)}"}
    
    return None, {"error": "Max retries exceeded"}


def print_mock_llm_output(transcript_data: Dict[str, Any], metadata: Dict[str, Any]) -> None:
    """
    Print mock LLM output as placeholder for Sprint P1.2.
    
    Args:
        transcript_data: Transcript information dictionary
        metadata: Video metadata dictionary
    """
    print("\n" + "="*60)
    print("MOCK LLM SUMMARIZATION OUTPUT (Placeholder for P1.2)")
    print("="*60)
    
    print(f"\n📊 **Transcript Statistics:**")
    print(f"  • Video: {metadata.get('title', 'Unknown')}")
    print(f"  • Channel: {metadata.get('channel', 'Unknown')}")
    print(f"  • Transcript language: {transcript_data.get('language', 'Unknown')}")
    print(f"  • Snippet count: {transcript_data.get('snippet_count', 0)}")
    print(f"  • Total duration: {transcript_data.get('total_duration', 0):.1f} seconds")
    print(f"  • Approx. word count: {len(transcript_data.get('total_text', '').split())}")
    
    print(f"\n🤖 **What would be sent to LLM:**")
    print(f"  • Provider: OpenRouter (via OpenAI SDK)")
    print(f"  • Model: gpt-4o-mini or similar")
    print(f"  • Prompt: 'Summarize this YouTube video transcript...'")
    print(f"  • Transcript length: {len(transcript_data.get('total_text', ''))} characters")
    print(f"  • Estimated tokens: ~{len(transcript_data.get('total_text', '')) // 4}")
    
    print(f"\n📝 **Mock Summary Output:**")
    print(f"  This is a placeholder summary for '{metadata.get('title', 'the video')}'.")
    print(f"  The actual LLM integration will be implemented in Sprint P1.2.")
    print(f"  The transcript contains {transcript_data.get('snippet_count', 0)} snippets")
    print(f"  covering {metadata.get('duration', 0)} seconds of content.")
    
    print("\n" + "="*60)
    print("END OF MOCK OUTPUT")
    print("="*60)


def print_real_llm_output(
    transcript_data: Dict[str, Any],
    metadata: Dict[str, Any],
    summary: str,
    stats: Dict[str, Any]
) -> None:
    """
    Print actual LLM output with summary and statistics.
    
    Args:
        transcript_data: Transcript information dictionary
        metadata: Video metadata dictionary
        summary: LLM-generated summary
        stats: LLM API statistics
    """
    print("\n" + "="*60)
    print("✅ REAL LLM SUMMARIZATION OUTPUT (Sprint P1.2)")
    print("="*60)
    
    print(f"\n📊 **Video Information:**")
    print(f"  • Title: {metadata.get('title', 'Unknown')}")
    print(f"  • Channel: {metadata.get('channel', 'Unknown')}")
    print(f"  • Duration: {metadata.get('duration', 0)} seconds")
    print(f"  • Views: {metadata.get('view_count', 0):,}")
    
    print(f"\n📝 **Transcript Statistics:**")
    print(f"  • Language: {transcript_data.get('language', 'Unknown')}")
    print(f"  • Snippet count: {transcript_data.get('snippet_count', 0)}")
    print(f"  • Total duration: {transcript_data.get('total_duration', 0):.1f} seconds")
    print(f"  • Word count: {len(transcript_data.get('total_text', '').split()):,}")
    print(f"  • Character count: {len(transcript_data.get('total_text', '')):,}")
    print(f"  • Token count: {stats.get('transcript_tokens', 0):,}")
    
    print(f"\n🤖 **LLM API Details:**")
    print(f"  • Provider: OpenRouter")
    print(f"  • Model: {stats.get('model', 'deepseek/deepseek-v3.2')}")
    print(f"  • Input tokens: {stats.get('input_tokens', 0):,}")
    print(f"  • Output tokens: {stats.get('output_tokens', 0):,}")
    print(f"  • Total tokens: {stats.get('total_tokens', 0):,}")
    print(f"  • Estimated cost: {stats.get('estimated_cost_usd', '$0.000000')}")
    print(f"  • Finish reason: {stats.get('finish_reason', 'unknown')}")
    
    print(f"\n" + "="*60)
    print("📋 **AI-GENERATED SUMMARY**")
    print("="*60)
    print(f"\n{summary}")
    
    print(f"\n" + "="*60)
    print("✅ SPRINT P1.2 COMPLETE: LLM Integration Successful")
    print("="*60)


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


def live_counter(prefix: str = "Elapsed") -> None:
    """Print a live counter that updates every second."""
    import threading
    import sys
    
    counter = [0]
    running = [True]
    
    def counter_thread():
        while running[0]:
            time.sleep(1)
            counter[0] += 1
            print(f"   {prefix}: {counter[0]}s", end="\r", flush=True)
    
    thread = threading.Thread(target=counter_thread, daemon=True)
    thread.start()
    
    return counter, running, thread


def main() -> None:
    """Main entry point for the script."""
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python poc_summarize.py <YOUTUBE_URL>")
        print("Example: python poc_summarize.py \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"")
        sys.exit(1)
    
    # Start overall timer
    overall_start = time.time()
    
    url = sys.argv[1]
    print(f"Processing YouTube URL: {url}")
    
    # Step 1: Extract video ID
    step_start = time.time()
    print("\n1. Extracting video ID...")
    video_id = extract_video_id(url)
    step_time = time.time() - step_start
    
    if not video_id:
        print(f"❌ Error: Could not extract video ID from URL: {url}")
        print("   Please check that the URL is a valid YouTube video URL.")
        print("   Supported formats:")
        print("   - https://www.youtube.com/watch?v=VIDEO_ID")
        print("   - https://youtu.be/VIDEO_ID")
        print("   - https://www.youtube.com/embed/VIDEO_ID")
        sys.exit(1)
    
    print(f"   ✓ Video ID extracted: {video_id} ({format_time(step_time)})")
    
    # Step 2: Fetch video metadata
    step_start = time.time()
    print("\n2. Fetching video metadata...")
    try:
        metadata = fetch_video_metadata(video_id)
        step_time = time.time() - step_start
        print(f"   ✓ Metadata fetched successfully ({format_time(step_time)})")
        print(f"   • Title: {metadata.get('title', 'Unknown')}")
        print(f"   • Channel: {metadata.get('channel', 'Unknown')}")
        print(f"   • Duration: {metadata.get('duration', 0)} seconds")
        print(f"   • Views: {metadata.get('view_count', 0):,}")
    except Exception as e:
        print(f"❌ Error fetching metadata: {str(e)}")
        print("   This could be due to:")
        print("   - Invalid video ID")
        print("   - Video is private or unavailable")
        print("   - Network connectivity issues")
        print("   - YouTube API restrictions")
        sys.exit(1)
    
    # Step 3: Fetch transcript
    step_start = time.time()
    print("\n3. Fetching transcript...")
    try:
        transcript_data = fetch_transcript(video_id)
        step_time = time.time() - step_start
        print(f"   ✓ Transcript fetched successfully ({format_time(step_time)})")
        print(f"   • Language: {transcript_data.get('language', 'Unknown')}")
        print(f"   • Snippets: {transcript_data.get('snippet_count', 0)}")
        print(f"   • Total duration: {transcript_data.get('total_duration', 0):.1f} seconds")
        
        # Show first few snippets as preview
        snippets = transcript_data.get('transcript', [])
        if snippets:
            print(f"   • First snippet: \"{snippets[0].get('text', '')[:50]}...\"")
        
    except TranscriptsDisabled as e:
        print(f"❌ Error: {str(e)}")
        print("   The video owner has disabled transcripts for this video.")
        print("   Try a different video with enabled captions.")
        sys.exit(1)
    except NoTranscriptFound as e:
        print(f"❌ Error: {str(e)}")
        print("   No transcript is available for this video.")
        print("   The video may not have captions in any language.")
        print("   Try a different video with available captions.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error fetching transcript: {str(e)}")
        print("   This could be due to:")
        print("   - Network connectivity issues")
        print("   - YouTube API restrictions")
        print("   - Permission issues")
        print("   - Rate limiting")
        sys.exit(1)
    
    # Step 4: Print success summary
    print("\n" + "="*60)
    print("✅ SUCCESS: Transcript retrieved and validated")
    print("="*60)
    print(f"\n📺 Video: {metadata.get('title', 'Unknown')}")
    print(f"👤 Channel: {metadata.get('channel', 'Unknown')}")
    print(f"🔤 Transcript: {transcript_data.get('snippet_count', 0)} snippets")
    print(f"   ({transcript_data.get('total_duration', 0):.1f} seconds, {transcript_data.get('language', 'Unknown')})")
    
    # Step 5: Call LLM for real summarization
    step_start = time.time()
    print("\n4. Calling LLM for summarization...")
    model = get_llm_model()
    model_display = model.split('/')[-1]
    print(f"   • Model: {model_display} via OpenRouter")
    print(f"   • Full model: {model}")
    print("   • Provider: OpenRouter (OpenAI-compatible API)")
    
    summary, stats = call_llm_summarize(
        transcript_text=transcript_data.get('total_text', ''),
        metadata=metadata
    )
    
    if summary and stats.get('success'):
        # Print real LLM output
        print_real_llm_output(transcript_data, metadata, summary, stats)
    else:
        # Fall back to mock output if LLM fails
        print(f"\n⚠️  LLM call failed: {stats.get('error', 'Unknown error')}")
        print("   Falling back to mock output for demonstration...")
        print_mock_llm_output(transcript_data, metadata)
        print(f"\n⚠️  Note: LLM integration encountered an error. Check API key and connectivity.")
    
    # Print total time
    total_time = time.time() - overall_start
    print(f"\n⏱️  Total processing time: {format_time(total_time)}")


if __name__ == "__main__":
    main()