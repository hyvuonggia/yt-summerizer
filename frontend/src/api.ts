import type { ApiError, SummarizeResponse, LanguageCode } from "./types";

const API_BASE_URL =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) ??
  "http://localhost:8000";

/**
 * Call the backend POST /api/summarize endpoint.
 * Throws an ApiError on non-2xx responses or network failures.
 */
export async function summarizeUrl(url: string, summaryLanguage: LanguageCode = "en"): Promise<SummarizeResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE_URL}/api/summarize`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url, summary_language: summaryLanguage }),
    });
  } catch (err) {
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
