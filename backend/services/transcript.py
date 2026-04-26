"""
Transcript service for fetching YouTube video transcripts.

This module handles:
- YouTube URL parsing and video ID extraction
- Transcript fetching using youtube-transcript-api
- Error handling for missing/disabled transcripts
"""

import re
import time
import threading
from typing import Optional, Dict, Any
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound

from ..config import settings


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


def _create_progress_counter(prefix: str = "Fetching"):
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


def fetch_transcript(video_id: str, language: str = "en") -> Dict[str, Any]:
    """
    Fetch transcript for a YouTube video.
    
    Args:
        video_id: YouTube video ID
        language: Preferred language code (default: "en")
        
    Returns:
        Dictionary with transcript data
        
    Raises:
        TranscriptsDisabled: When transcripts are disabled for the video
        NoTranscriptFound: When no transcript is available
        Exception: For other errors (network, permission, etc.)
    """
    # Live counter for progress
    counter, running, thread = _create_progress_counter("Fetching transcript")
    
    try:
        # Create API instance
        ytt_api = YouTubeTranscriptApi()
        
        # Try to fetch transcript in preferred language
        try:
            # First try to list transcripts to get metadata
            transcript_list = ytt_api.list(video_id)
            transcript = transcript_list.find_transcript([language])
            fetched_transcript = transcript.fetch()
            
            # Extract metadata from transcript object
            language_name = transcript.language
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
            fetched_transcript = ytt_api.fetch(video_id, languages=[language])
            
            # Convert to list of dictionaries
            snippets_list = []
            for snippet in fetched_transcript:
                snippets_list.append({
                    'text': snippet.text,
                    'start': snippet.start,
                    'duration': snippet.duration
                })
            snippets = snippets_list
            language_name = "English" if language == "en" else language
            language_code = language
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
        
        # Stop counter
        running[0] = False
        thread.join(timeout=0.1)
        print(f"   Fetching transcript... ({counter[0]}s) - Done")
        
        return {
            'success': True,
            'video_id': video_id,
            'language': language_name,
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


def validate_youtube_url(url: str) -> Dict[str, Any]:
    """
    Validate a YouTube URL and extract video ID.
    
    Args:
        url: YouTube URL to validate
        
    Returns:
        Dictionary with validation results
    """
    if not url:
        return {
            'valid': False,
            'error': 'URL is required',
            'error_code': 'MISSING_URL'
        }
    
    video_id = extract_video_id(url)
    
    if not video_id:
        return {
            'valid': False,
            'error': f'Could not extract video ID from URL: {url}',
            'error_code': 'INVALID_URL',
            'suggested_formats': [
                'https://www.youtube.com/watch?v=VIDEO_ID',
                'https://youtu.be/VIDEO_ID',
                'https://www.youtube.com/embed/VIDEO_ID'
            ]
        }
    
    return {
        'valid': True,
        'video_id': video_id,
        'url': url
    }