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
// Auth API (TSK-0303)
// ============================================

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserInfo {
  id: number;
  email: string;
  username: string;
  created_at: string;
}

export interface AuthResponse {
  success: boolean;
  user: UserInfo;
  token: TokenResponse;
}

// Token storage key
const TOKEN_KEY = "yt_summarizer_token";

/**
 * Get stored authentication token.
 */
export function getStoredToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

/**
 * Store authentication token.
 */
export function storeToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

/**
 * Remove stored authentication token.
 */
export function removeStoredToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

/**
 * Check if user is authenticated.
 */
export function isAuthenticated(): boolean {
  return getStoredToken() !== null;
}

/**
 * Register a new user.
 */
export async function registerUser(
  email: string,
  password: string,
  username?: string
): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password, username }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const apiError: ApiError = {
      code: body?.detail?.error_code || "REGISTRATION_FAILED",
      message: body?.detail?.error || "Registration failed",
      status: response.status,
    };
    throw apiError;
  }

  const data = (await response.json()) as AuthResponse;
  storeToken(data.token.access_token);
  return data;
}

/**
 * Login with email and password.
 */
export async function loginUser(email: string, password: string): Promise<TokenResponse> {
  const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const apiError: ApiError = {
      code: body?.detail?.error_code || "LOGIN_FAILED",
      message: body?.detail?.error || "Invalid credentials",
      status: response.status,
    };
    throw apiError;
  }

  const data = (await response.json()) as TokenResponse;
  storeToken(data.access_token);
  return data;
}

/**
 * Logout user (remove token).
 */
export function logoutUser(): void {
  removeStoredToken();
}

// ============================================
// History API (TSK-0302)
// ============================================

export interface HistoryItem {
  id: number;
  video_id: string;
  video_title: string;
  summary: string;
  created_at: string;
}

export interface HistoryListResponse {
  items: HistoryItem[];
  total: number;
}

/**
 * Get user's summary history (requires auth).
 */
export async function getUserHistory(): Promise<HistoryListResponse> {
  const token = getStoredToken();
  if (!token) {
    const apiError: ApiError = {
      code: "NOT_AUTHENTICATED",
      message: "Not authenticated",
      status: 401,
    };
    throw apiError;
  }

  const response = await fetch(`${API_BASE_URL}/api/history`, {
    method: "GET",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    const apiError: ApiError = {
      code: body?.detail?.error_code || "HISTORY_FAILED",
      message: body?.detail?.error || "Failed to fetch history",
      status: response.status,
    };
    throw apiError;
  }

  return (await response.json()) as HistoryListResponse;
}

/**
 * Delete a summary from history.
 */
export async function deleteHistoryItem(summaryId: number): Promise<void> {
  const token = getStoredToken();
  if (!token) {
    throw new Error("Not authenticated");
  }

  const response = await fetch(`${API_BASE_URL}/api/history/${summaryId}`, {
    method: "DELETE",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok) {
    throw new Error("Failed to delete history item");
  }
}

// ============================================
// Summarize API (Existing)
// ============================================

/**
 * Call the backend POST /api/summarize endpoint.
 * Throws an ApiError on non-2xx responses or network failures.
 */
export async function summarizeUrl(url: string, summaryLanguage: LanguageCode = "en"): Promise<SummarizeResponse> {
  const token = getStoredToken();
  if (!token) {
    const apiError: ApiError = {
      code: "NOT_AUTHENTICATED",
      message: "Not authenticated",
      status: 401,
    };
    throw apiError;
  }

  let response: Response;
  try {
    response = await fetchWithTimeout(`${API_BASE_URL}/api/summarize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
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
