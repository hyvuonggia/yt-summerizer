import type { ApiError, SummarizeResponse, LanguageCode } from "./types";

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://localhost:8000";

// Timeout configuration (in ms)
const REQUEST_TIMEOUT = 60000; // 60 seconds - generous for AI summarize calls

/**
 * AbortController-based fetch with timeout.
 * Throws ApiError with TIMEOUT code on timeout.
 */
async function fetchWithTimeout(
  url: string,
  options: RequestInit = {}
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
    });
    return response;
  } catch (err) {
    // Check for abort by name or message (more robust across environments)
    const isAbort = err instanceof Error && (
      err.name === "AbortError" || 
      err.message?.includes("aborted")
    );
    if (isAbort) {
      const apiError: ApiError = {
        code: "TIMEOUT",
        message: "The request timed out. Please try again.",
        status: 0,
      };
      throw apiError;
    }
    throw err;
  } finally {
    clearTimeout(timeoutId);
  }
}

// ============================================
// Summarize API (Open Access)
// ============================================

/**
 * Call the backend POST /api/summarize endpoint.
 * No authentication required.
 * Throws an ApiError on non-2xx responses or network failures.
 */
export async function summarizeUrl(url: string, summaryLanguage: LanguageCode = "en"): Promise<SummarizeResponse> {
  let response: Response;
  try {
    response = await fetchWithTimeout(`${API_BASE_URL}/api/summarize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ url, summary_language: summaryLanguage }),
    });
  } catch (err) {
    if ((err as ApiError).code === "TIMEOUT") {
      throw err; // Already formatted as ApiError
    }
    const apiError: ApiError = {
      code: "NETWORK_ERROR",
      message:
        err instanceof Error
          ? err.message
          : "Could not reach the server. Check your connection.",
      status: 0,
    };
    throw apiError;
  }

  if (!response.ok) {
    let code = "UNKNOWN_ERROR";
    let message = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      const detail = body?.detail;
      if (detail && typeof detail === "object") {
        if (typeof detail.error_code === "string") code = detail.error_code;
        if (typeof detail.error === "string") message = detail.error;
      } else if (typeof detail === "string") {
        message = detail;
      }
    } catch {
      // body not JSON — keep defaults
    }
    const apiError: ApiError = { code, message, status: response.status };
    throw apiError;
  }

  return (await response.json()) as SummarizeResponse;
}