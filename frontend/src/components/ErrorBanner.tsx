import type { ApiError } from "../types";

interface ErrorBannerProps {
  error: ApiError | null;
}

/**
 * Maps a backend error code to a user-friendly message.
 * Returns null when there's no friendly mapping.
 */
function friendlyMessage(error: ApiError): string {
  switch (error.code) {
    case "INVALID_URL":
    case "MISSING_URL":
      return "Invalid YouTube URL. Please paste a valid video link.";
    case "NO_SUBTITLES_AVAILABLE":
      return "No subtitles are available for this video. Try a different one.";
    case "TRANSCRIPTS_DISABLED":
      return "Transcripts are disabled for this video.";
    case "VIDEO_NOT_FOUND":
      return "We couldn't find that video. Double-check the URL.";
    case "VIDEO_PRIVATE":
      return "This video is private and cannot be summarized.";
    case "LLM_RATE_LIMITED":
      return "The AI provider is rate-limited right now. Please retry shortly.";
    case "LLM_TIMEOUT":
      return "Summarization timed out. Please try again.";
    case "LLM_API_ERROR":
      return "The AI provider returned an error. Please try again.";
    case "NETWORK_ERROR":
      return "Could not reach the server. Check your connection and try again.";
    default:
      if (error.message) return error.message;
      if (error.status >= 500) return "Server error, please try again.";
      return "Something went wrong. Please try again.";
  }
}

export function ErrorBanner({ error }: ErrorBannerProps) {
  if (!error) return null;
  return (
    <div role="alert" className="error-banner">
      <strong>Error:</strong> {friendlyMessage(error)}
    </div>
  );
}
