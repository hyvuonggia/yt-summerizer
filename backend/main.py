#!/usr/bin/env python3
"""
FastAPI Backend for YouTube Video Summarizer

This is the main entry point for the FastAPI backend application.
It sets up the API server with CORS, routes, and middleware.

Sprint P2.1: Backend API Skeleton + Core Summarize Endpoint
Sprint P2.3: CORS/API Setup + Basic Operational Hardening
"""

import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .models import SummarizeRequest, SummarizeResponse, ErrorResponse
from .services.transcript import extract_video_id, fetch_transcript
from .services.metadata import fetch_video_metadata
from .services.summarization import call_llm_summarize
from .services.token_counter import count_tokens, truncate_text_to_tokens

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    logger.info("Starting YouTube Video Summarizer Backend")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"LLM Model: {settings.llm_model}")
    logger.info(f"CORS Origins: {settings.cors_origins}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down YouTube Video Summarizer Backend")


# Create FastAPI app with lifespan
app = FastAPI(
    title="YouTube Video Summarizer API",
    description="API for summarizing YouTube videos using AI",
    version="0.1.0",
    lifespan=lifespan,
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "YouTube Video Summarizer API",
        "version": "0.1.0",
        "status": "running",
        "endpoints": {
            "POST /api/summarize": "Summarize a YouTube video",
            "GET /health": "Health check endpoint",
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.environment,
    }


@app.post("/api/summarize", response_model=SummarizeResponse)
async def summarize_video(request: SummarizeRequest):
    """
    Summarize a YouTube video.
    
    This endpoint:
    1. Validates the YouTube URL and extracts video ID
    2. Fetches video metadata (title, channel, etc.)
    3. Retrieves the transcript (subtitles)
    4. Calls LLM to generate a summary
    5. Returns structured summary response
    
    Returns 400 for invalid URLs, 422 for missing subtitles.
    """
    import time
    from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
    
    start_time = time.time()
    request_start = datetime.now().isoformat()
    
    logger.info(f"Request started: POST /api/summarize - URL: {request.url}")

    # Step 1: Validate URL and extract video ID (TSK-0202)
    video_id = extract_video_id(request.url)
    if not video_id:
        logger.warning(f"Invalid URL - could not extract video ID: {request.url}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Could not extract video ID from URL: {request.url}",
                "error_code": "INVALID_URL",
                "suggested_formats": [
                    "https://www.youtube.com/watch?v=VIDEO_ID",
                    "https://youtu.be/VIDEO_ID",
                    "https://www.youtube.com/embed/VIDEO_ID"
                ]
            }
        )
    logger.info(f"Video ID extracted: {video_id}")

    # Step 2: Fetch video metadata (TSK-0203 - metadata needed for context)
    logger.info(f"Fetching metadata for video: {video_id}")
    try:
        metadata = fetch_video_metadata(video_id)
    except Exception as e:
        logger.error(f"Metadata fetch failed for video {video_id}: {e}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": f"Could not fetch video metadata: {str(e)}",
                "error_code": "VIDEO_NOT_FOUND",
                "video_id": video_id
            }
        )
    logger.info(f"Metadata fetched - Title: {metadata.get('title', 'Unknown')}, Channel: {metadata.get('channel', 'Unknown')}")

    # Step 3: Fetch transcript (TSK-0203)
    logger.info(f"Fetching transcript for video: {video_id}")
    try:
        transcript_data = fetch_transcript(video_id, language=request.language or "en")
    except TranscriptsDisabled:
        logger.warning(f"Transcripts disabled for video: {video_id}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "Transcripts are disabled for this video",
                "error_code": "TRANSCRIPTS_DISABLED",
                "video_id": video_id
            }
        )
    except NoTranscriptFound:
        logger.warning(f"No subtitles available for video: {video_id}")
        raise HTTPException(
            status_code=422,
            detail={
                "error": "No subtitles available for this video",
                "error_code": "NO_SUBTITLES_AVAILABLE",
                "video_id": video_id,
                "suggested_action": "Try a different video with enabled captions"
            }
        )
    except Exception as e:
        logger.error(f"Transcript fetch error for video {video_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Error fetching transcript: {str(e)}",
                "error_code": "TRANSCRIPT_ERROR",
                "video_id": video_id
            }
        )
    
    # Log transcript outcome (NOT the content)
    logger.info(f"Transcript fetched - Language: {transcript_data.get('language', 'Unknown')} ({transcript_data.get('language_code', '?')}), "
                f"Auto-generated: {transcript_data.get('is_generated', False)}, "
                f"Snippets: {transcript_data.get('snippet_count', 0)}")

    # Step 4: Calculate transcript stats (TSK-0205 - token truncation)
    transcript_text = transcript_data.get('total_text', '')
    word_count = len(transcript_text.split())
    char_count = len(transcript_text)
    logger.info(f"Transcript stats - Words: {word_count:,}, Characters: {char_count:,}")

    # Step 5: Call LLM summarization (TSK-0204)
    # Get summary language from request, validate and default to English
    from ..models import SUPPORTED_SUMMARY_LANGUAGES
    summary_lang = request.summary_language or "en"
    if summary_lang not in SUPPORTED_SUMMARY_LANGUAGES:
        logger.warning(f"Unsupported summary_language '{summary_lang}', defaulting to 'en'")
        summary_lang = "en"
    logger.info(f"Calling LLM ({settings.llm_model}) for video: {video_id} - Summary language: {summary_lang}")
    llm_start = time.time()
    try:
        summary, llm_stats = call_llm_summarize(transcript_text, metadata, summary_language=summary_lang)
    except Exception as e:
        logger.error(f"LLM call failed for video {video_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": f"Error during summarization: {str(e)}",
                "error_code": "LLM_API_ERROR",
                "video_id": video_id
            }
        )

    if not summary:
        err = llm_stats.get("error", "Summarization failed")
        logger.error(f"LLM returned no summary for video {video_id}: {err}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": err,
                "error_code": llm_stats.get("error_code", "LLM_API_ERROR"),
                "video_id": video_id
            }
        )
    
    # Log LLM latency and stats (NOT the summary content)
    llm_latency = time.time() - llm_start
    logger.info(f"LLM response - Model: {llm_stats.get('model', settings.llm_model)}, "
                f"Tokens: {llm_stats.get('total_tokens', 0):,} "
                f"(in: {llm_stats.get('input_tokens', 0):,} / out: {llm_stats.get('output_tokens', 0):,}), "
                f"Cost: {llm_stats.get('estimated_cost_usd', '$?')}, "
                f"Latency: {llm_latency:.1f}s")

    # Calculate processing time
    processing_time = time.time() - start_time
    request_end = datetime.now().isoformat()
    
    logger.info(f"Request completed - Video: {video_id}, Processing time: {processing_time:.1f}s")

    # Step 6: Build response (TSK-0206)
    from .models import VideoMetadata, TranscriptData, LLMStats
    
    # Build VideoMetadata
    video_metadata = VideoMetadata(
        video_id=metadata.get('video_id', video_id),
        title=metadata.get('title', 'Unknown'),
        channel=metadata.get('channel', 'Unknown'),
        channel_id=metadata.get('channel_id'),
        duration=metadata.get('duration', 0),
        view_count=metadata.get('view_count'),
        upload_date=metadata.get('upload_date'),
        description=metadata.get('description'),
        thumbnail=metadata.get('thumbnail'),
        categories=metadata.get('categories', []),
        tags=metadata.get('tags', [])
    )
    
    # Build TranscriptData
    transcript_stats_model = TranscriptData(
        video_id=video_id,
        language=transcript_data.get('language', 'English'),
        language_code=transcript_data.get('language_code', 'en'),
        is_generated=transcript_data.get('is_generated', False),
        snippet_count=transcript_data.get('snippet_count', 0),
        total_duration=transcript_data.get('total_duration', 0.0),
        total_text=transcript_text[:500] + "..." if len(transcript_text) > 500 else transcript_text,  # Truncate for response
        word_count=word_count,
        character_count=char_count,
        token_count=llm_stats.get('transcript_tokens')
    )
    
    # Build LLMStats
    llm_stats_model = LLMStats(
        model=llm_stats.get('model', 'unknown'),
        provider=llm_stats.get('provider', 'openrouter'),
        input_tokens=llm_stats.get('input_tokens', 0),
        output_tokens=llm_stats.get('output_tokens', 0),
        total_tokens=llm_stats.get('total_tokens', 0),
        finish_reason=llm_stats.get('finish_reason', 'unknown'),
        estimated_cost_usd=llm_stats.get('estimated_cost_usd', '$0.00'),
        api_time=llm_stats.get('api_time', 0.0)
    )
    
    return SummarizeResponse(
        success=True,
        summary=summary,
        video_id=video_id,
        metadata=video_metadata,
        transcript_stats=transcript_stats_model,
        llm_stats=llm_stats_model,
        processing_time=processing_time,
        timestamp=request_end
    )


if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting development server...")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )