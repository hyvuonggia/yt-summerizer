#!/usr/bin/env python3
"""
FastAPI Backend for YouTube Video Summarizer

This is the main entry point for the FastAPI backend application.
It sets up the API server with CORS, routes, and middleware.

Sprint P2.1: Backend API Skeleton + Core Summarize Endpoint
"""

import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .config import settings
from .models import SummarizeRequest, SummarizeResponse, ErrorResponse
from .services.transcript import extract_video_id, fetch_transcript
from .services.metadata import fetch_video_metadata
from .services.summarization import call_llm_summarize
from .services.token_counter import count_tokens, truncate_text_to_tokens


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    # Startup
    print(f"🚀 Starting YouTube Video Summarizer Backend")
    print(f"   Environment: {settings.environment}")
    print(f"   LLM Provider: {settings.llm_provider}")
    print(f"   LLM Model: {settings.llm_model}")
    print(f"   CORS Origins: {settings.cors_origins}")
    
    yield
    
    # Shutdown
    print("👋 Shutting down YouTube Video Summarizer Backend")


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
    return {
        "status": "healthy",
        "timestamp": "TODO: Add timestamp",
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
    # TODO: Implement actual summarization logic
    # For now, return a placeholder response
    raise HTTPException(
        status_code=501,
        detail="Summarization endpoint not yet implemented. This is a skeleton for Sprint P2.1."
    )


if __name__ == "__main__":
    import uvicorn
    
    print("Starting development server...")
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )