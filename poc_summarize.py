#!/usr/bin/env python3
"""
YouTube Video Summarizer - Proof of Concept (Sprint P1.1)

This script implements transcript retrieval and validation for YouTube videos.
It extracts video ID from URL, fetches transcript, retrieves metadata,
and handles error cases with clear messages.

Usage:
    python poc_summarize.py <YOUTUBE_URL>

Example:
    python poc_summarize.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
"""

import sys
import re
from typing import Optional, Dict, Any, List
from urllib.parse import urlparse, parse_qs

# Third-party imports
try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    import yt_dlp
except ImportError as e:
    print(f"Error: Missing required dependency - {e}")
    print("Please install dependencies: pip install youtube-transcript-api yt-dlp")
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
        raise TranscriptsDisabled(f"Transcripts are disabled for video {video_id}") from e
    except NoTranscriptFound as e:
        raise NoTranscriptFound(f"No transcript found for video {video_id}") from e
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
    url = f"https://www.youtube.com/watch?v={video_id}"
    
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'skip_download': True,
        'extract_flat': False,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
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
        raise Exception(f"Invalid URL or video not found: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching metadata: {str(e)}")


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


def main() -> None:
    """Main entry point for the script."""
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python poc_summarize.py <YOUTUBE_URL>")
        print("Example: python poc_summarize.py \"https://www.youtube.com/watch?v=dQw4w9WgXcQ\"")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"Processing YouTube URL: {url}")
    
    # Step 1: Extract video ID
    print("\n1. Extracting video ID...")
    video_id = extract_video_id(url)
    
    if not video_id:
        print(f"❌ Error: Could not extract video ID from URL: {url}")
        print("   Please check that the URL is a valid YouTube video URL.")
        print("   Supported formats:")
        print("   - https://www.youtube.com/watch?v=VIDEO_ID")
        print("   - https://youtu.be/VIDEO_ID")
        print("   - https://www.youtube.com/embed/VIDEO_ID")
        sys.exit(1)
    
    print(f"   ✓ Video ID extracted: {video_id}")
    
    # Step 2: Fetch video metadata
    print("\n2. Fetching video metadata...")
    try:
        metadata = fetch_video_metadata(video_id)
        print(f"   ✓ Metadata fetched successfully")
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
    print("\n3. Fetching transcript...")
    try:
        transcript_data = fetch_transcript(video_id)
        print(f"   ✓ Transcript fetched successfully")
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
    
    # Step 5: Print mock LLM output
    print_mock_llm_output(transcript_data, metadata)
    
    print(f"\n🎯 Ready for Sprint P1.2: LLM integration")


if __name__ == "__main__":
    main()