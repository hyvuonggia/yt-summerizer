import type { ApiError } from "../types";

interface ErrorBannerProps {
  error: ApiError | null;
}

/** Error message with optional action hint */
interface ErrorInfo {
  message: string;
  action?: string;
}

/**
 * Maps a backend error code to a user-friendly message with optional action.
 */
function getErrorInfo(error: ApiError): ErrorInfo {
  switch (error.code) {
    case "INVALID_URL":
    case "MISSING_URL":
      return {
        message: "Invalid YouTube URL.",
        action: "Paste a valid YouTube link (e.g., youtube.com/watch?v=...)",
      };
    case "NO_SUBTITLES_AVAILABLE":
      return {
        message: "No subtitles are available for this video.",
        action: "Try a different YouTube video that has closed captions.",
      };
    case "TRANSCRIPTS_DISABLED":
      return {
        message: "Transcripts are disabled for this video.",
        action: "This video's owner has disabled transcripts.",
      };
    case "VIDEO_NOT_FOUND":
      return {
        message: "We couldn't find that video.",
        action: "Double-check the URL and try again.",
      };
    case "VIDEO_PRIVATE":
      return {
        message: "This video is private and cannot be summarized.",
        action: "Choose a public video instead.",
      };
    case "LLM_RATE_LIMITED":
      return {
        message: "The AI provider is rate-limited right now.",
        action: "Wait a moment and try again.",
      };
    case "LLM_TIMEOUT":
      return {
        message: "Summarization timed out.",
        action: "The video may be too long. Try a shorter one.",
      };
    case "LLM_API_ERROR":
      return {
        message: "The AI provider returned an error.",
        action: "Try again in a few seconds.",
      };
    case "TIMEOUT":
      return {
        message: "The request took too long.",
        action: "The video may be very long. Try a different one.",
      };
    case "NETWORK_ERROR":
      return {
        message: "Could not reach the server.",
        action: "Check your internet connection and try again.",
      };
    case "NOT_AUTHENTICATED":
      return {
        message: "Please log in to summarize videos.",
        action: "Sign in or register to continue.",
      };
    default:
      // Show custom message from backend if provided (takes priority)
      if (error.message) {
        const isServerError = error.status >= 500;
        return {
          message: error.message,
          action: isServerError
            ? "If the problem persists, try again in a few minutes."
            : "Try again or try a different video.",
        };
      }
      // Generic server error for 5xx with no message
      if (error.status >= 500) {
        return {
          message: "Server error. Please try again later.",
          action: "If the problem persists, try again in a few minutes.",
        };
      }
      return {
        message: "Something went wrong.",
        action: "Try again or try a different video.",
      };
  }
}

export function ErrorBanner({ error }: ErrorBannerProps) {
  if (!error) return null;
  const { message, action } = getErrorInfo(error);
  return (
    <div role="alert" className="error-banner">
      <strong>Error:</strong> {message}
      {action && <span className="error-action">{action}</span>}
    </div>
  );
}
