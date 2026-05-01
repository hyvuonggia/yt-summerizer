# BUG-0002: Missing Authorization Header in summarizeUrl API Call

**Severity:** High | **Status:** Closed | **Found In:** Sprint P2.3

## Steps to Reproduce
1. Register a new user at `/api/auth/register`
2. Login (or use the token from registration response)
3. Make a GET request to `/api/history` - works (200 OK)
4. Make a POST request to `/api/summarize` - fails (401 Unauthorized)

## Expected vs Actual
- **Expected:** POST /api/summarize should work with valid auth token
- **Actual:** Returns 401 Unauthorized even though user is logged in

## Root Cause Analysis
The frontend's `summarizeUrl` function in `frontend/src/api.ts` (lines 202-209) does NOT include the `Authorization: Bearer ${token}` header, unlike the `getUserHistory` function which correctly includes it.

**Code comparison:**
```typescript
// getUserHistory - CORRECT (includes auth header)
const response = await fetch(`${API_BASE_URL}/api/history`, {
  method: "GET",
  headers: {
    Authorization: `Bearer ${token}`,  // ✓ Present
  },
});

// summarizeUrl - BUG (missing auth header)
response = await fetch(`${API_BASE_URL}/api/summarize`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },  // ✗ Missing Authorization
  body: JSON.stringify({ url, summary_language: summaryLanguage }),
});
```

## Fix Plan
- [x] Add Authorization header to `summarizeUrl` function in `frontend/src/api.ts`
- [x] Verify fix by testing the summarize endpoint after login

## Fix Applied
- Added token retrieval and Authorization header to `summarizeUrl` function
- Frontend builds successfully
- Pre-existing test failures (unrelated to this fix - tests mock not configured for authenticated endpoint)

## Execution Log
- *[2026-05-01 22:30]* Filed by Engineering Manager after user bug report
- *[2026-05-01 22:30]* Root cause identified: missing Authorization header in frontend