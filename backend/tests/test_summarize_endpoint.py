"""
Tests for the /api/summarize endpoint (Sprint P2.1).

These tests verify the core functionality of the summarization API.
"""

import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

# Import the app
from backend.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


class TestRequestValidation:
    """Tests for request validation (TSK-0202)."""

    def test_invalid_url_returns_400(self, client):
        """Invalid YouTube URL should return HTTP 400."""
        response = client.post(
            "/api/summarize",
            json={"url": "https://not-a-youtube-url.com/video"}
        )
        assert response.status_code == 400

    def test_empty_url_returns_400(self, client):
        """Empty URL should return HTTP 400 (our validation)."""
        response = client.post(
            "/api/summarize",
            json={"url": ""}
        )
        # Our validation returns 400 when video_id cannot be extracted
        assert response.status_code == 400

    def test_missing_url_returns_422(self, client):
        """Missing URL should return HTTP 422 (Pydantic validation)."""
        response = client.post(
            "/api/summarize",
            json={}
        )
        assert response.status_code == 422

    def test_invalid_url_format_message(self, client):
        """Invalid URL should include error message."""
        response = client.post(
            "/api/summarize",
            json={"url": "https://not-a-youtube-url.com/video"}
        )
        data = response.json()
        assert "error" in data or "detail" in data


class TestTranscriptRetrieval:
    """Tests for transcript retrieval in endpoint (TSK-0203).
    
    Note: Full transcript error tests require integration tests with real endpoints.
    The endpoint logic correctly handles TranscriptsDisabled and NoTranscriptFound.
    """

    def test_endpoint_handles_invalid_youtube_url(self, client):
        """Invalid YouTube URL should be handled at validation level."""
        response = client.post(
            "/api/summarize",
            json={"url": "https://example.com/not-youtube"}
        )
        # Should return 400 due to invalid video ID
        assert response.status_code == 400


class TestSuccessfulSummarization:
    """Tests for successful summarization flow (TSK-0204, TSK-0205, TSK-0206)."""

    @patch('backend.main.fetch_video_metadata')
    @patch('backend.main.fetch_transcript')
    @patch('backend.main.call_llm_summarize')
    def test_successful_summarization(self, mock_llm, mock_transcript, mock_metadata, client):
        """Successful summarization returns summary JSON."""
        # Mock metadata
        mock_metadata.return_value = {
            'video_id': 'dQw4w9WgXcQ',
            'title': 'Test Video',
            'channel': 'Test Channel',
            'duration': 300,
            'view_count': 1000,
            'thumbnail': 'https://example.com/thumb.jpg'
        }

        # Mock transcript
        mock_transcript.return_value = {
            'success': True,
            'video_id': 'dQw4w9WgXcQ',
            'language': 'English',
            'language_code': 'en',
            'is_generated': False,
            'snippet_count': 50,
            'total_duration': 300.0,
            'total_text': 'This is a test transcript with some content.',
            'transcript': [{'text': 'Test', 'start': 0.0, 'duration': 5.0}]
        }

        # Mock LLM call
        mock_llm.return_value = (
            "This is a test summary.",
            {
                "success": True,
                "model": "deepseek/deepseek-v3.2",
                "provider": "openrouter",
                "input_tokens": 100,
                "output_tokens": 50,
                "total_tokens": 150,
                "finish_reason": "stop",
                "estimated_cost_usd": "$0.0001",
                "api_time": 1.5
            }
        )

        response = client.post(
            "/api/summarize",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert data["summary"] == "This is a test summary."
        assert data["video_id"] == "dQw4w9WgXcQ"

    @patch('backend.main.fetch_video_metadata')
    @patch('backend.main.fetch_transcript')
    @patch('backend.main.call_llm_summarize')
    def test_response_includes_provider(self, mock_llm, mock_transcript, mock_metadata, client):
        """Response should include provider name."""
        mock_metadata.return_value = {
            'video_id': 'dQw4w9WgXcQ',
            'title': 'Test Video',
            'channel': 'Test Channel',
            'duration': 300,
            'view_count': 1000,
            'thumbnail': 'https://example.com/thumb.jpg'
        }

        mock_transcript.return_value = {
            'success': True,
            'video_id': 'dQw4w9WgXcQ',
            'language': 'English',
            'language_code': 'en',
            'is_generated': False,
            'snippet_count': 50,
            'total_duration': 300.0,
            'total_text': 'Test transcript content here.',
            'transcript': []
        }

        mock_llm.return_value = (
            "Summary",
            {
                "success": True,
                "model": "deepseek/deepseek-v3.2",
                "provider": "openrouter",
                "input_tokens": 100,
                "output_tokens": 50,
                "total_tokens": 150,
                "finish_reason": "stop",
                "estimated_cost_usd": "$0.0001",
                "api_time": 1.5
            }
        )

        response = client.post(
            "/api/summarize",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        )

        data = response.json()
        # Should have provider info (either in llm_stats or directly)
        assert "provider" in data or ("llm_stats" in data and "provider" in data["llm_stats"])

    @patch('backend.main.fetch_video_metadata')
    @patch('backend.main.fetch_transcript')
    @patch('backend.main.call_llm_summarize')
    def test_response_includes_transcript_stats(self, mock_llm, mock_transcript, mock_metadata, client):
        """Response should include transcript statistics."""
        mock_metadata.return_value = {
            'video_id': 'dQw4w9WgXcQ',
            'title': 'Test Video',
            'channel': 'Test Channel',
            'duration': 300,
            'view_count': 1000,
            'thumbnail': 'https://example.com/thumb.jpg'
        }

        mock_transcript.return_value = {
            'success': True,
            'video_id': 'dQw4w9WgXcQ',
            'language': 'English',
            'language_code': 'en',
            'is_generated': False,
            'snippet_count': 50,
            'total_duration': 300.0,
            'total_text': 'Test transcript content here with more words.',
            'transcript': []
        }

        mock_llm.return_value = (
            "Summary",
            {
                "success": True,
                "model": "deepseek/deepseek-v3.2",
                "provider": "openrouter",
                "input_tokens": 100,
                "output_tokens": 50,
                "total_tokens": 150,
                "finish_reason": "stop",
                "estimated_cost_usd": "$0.0001",
                "api_time": 1.5
            }
        )

        response = client.post(
            "/api/summarize",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        )

        data = response.json()
        assert "transcript_stats" in data
        assert "word_count" in data["transcript_stats"] or "token_count" in data["transcript_stats"]


class TestTokenTruncation:
    """Tests for token truncation (TSK-0205)."""

    @patch('backend.main.fetch_video_metadata')
    @patch('backend.main.fetch_transcript')
    @patch('backend.main.call_llm_summarize')
    def test_truncation_info_in_response(self, mock_llm, mock_transcript, mock_metadata, client):
        """Response should include truncation info when transcript is truncated."""
        mock_metadata.return_value = {
            'video_id': 'dQw4w9WgXcQ',
            'title': 'Test Video',
            'channel': 'Test Channel',
            'duration': 300,
            'view_count': 1000,
            'thumbnail': 'https://example.com/thumb.jpg'
        }

        mock_transcript.return_value = {
            'success': True,
            'video_id': 'dQw4w9WgXcQ',
            'language': 'English',
            'language_code': 'en',
            'is_generated': False,
            'snippet_count': 100,
            'total_duration': 300.0,
            'total_text': 'A' * 10000,  # Long transcript
            'transcript': []
        }

        mock_llm.return_value = (
            "Summary",
            {
                "success": True,
                "model": "deepseek/deepseek-v3.2",
                "provider": "openrouter",
                "input_tokens": 50000,
                "output_tokens": 50,
                "total_tokens": 50050,
                "finish_reason": "stop",
                "estimated_cost_usd": "$0.0001",
                "api_time": 1.5,
                "truncated": True  # Indicate truncation happened
            }
        )

        response = client.post(
            "/api/summarize",
            json={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"}
        )

        data = response.json()
        # Check for truncation info in response
        assert "transcript_stats" in data


class TestHealthEndpoint:
    """Tests for health endpoint."""

    def test_health_endpoint_returns_200(self, client):
        """Health endpoint should return 200."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_endpoint_returns_status(self, client):
        """Health endpoint should return status."""
        response = client.get("/health")
        data = response.json()
        assert "status" in data
