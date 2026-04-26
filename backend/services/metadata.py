"""
Metadata service for fetching YouTube video information.

This module handles:
- Video metadata extraction using yt-dlp
- Title, channel, duration, view count, etc.
- Error handling for unavailable videos
"""

import time
import threading
from typing import Dict, Any

import yt_dlp
from yt_dlp.utils import DownloadError

from ..config import settings


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
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': False,
        'socket_timeout': settings.youtube_timeout,
    }
    
    # Live counter for progress
    counter, running, thread = _create_progress_counter("Fetching metadata")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        
        # Stop counter
        running[0] = False
        thread.join(timeout=0.1)
        print(f"   Fetching metadata... ({counter[0]}s) - Done")
        
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
        
    except DownloadError as e:
        running[0] = False
        raise Exception(f"Invalid URL or video not found: {str(e)}")
    except Exception as e:
        running[0] = False
        raise Exception(f"Error fetching metadata: {str(e)}")


def get_basic_metadata(video_id: str) -> Dict[str, Any]:
    """
    Get basic metadata with minimal error handling.
    
    This is a simpler version that returns defaults if metadata fetch fails.
    
    Args:
        video_id: YouTube video ID
        
    Returns:
        Dictionary with at least basic metadata
    """
    try:
        return fetch_video_metadata(video_id)
    except Exception as e:
        # Return minimal metadata on failure
        return {
            'success': False,
            'video_id': video_id,
            'title': 'Unknown',
            'channel': 'Unknown',
            'duration': 0,
            'view_count': 0,
            'error': str(e)
        }