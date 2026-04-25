# YouTube Video Summarizer Web App Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a web application where users paste a YouTube URL and receive an AI-generated summary of the video.

**Architecture:** Split the system into a React frontend and a Python (FastAPI) backend. The backend is responsible for URL validation, transcript acquisition (or fallback), LLM summarization, and returning a structured response. Keep Phase 1 minimal (CLI/script proving end-to-end), then evolve to a production-ready API with robust error handling for Phase 2, and finally add user/auth/storage/provider selection in Phase 3.

**Tech Stack:**
- Frontend: React (TypeScript optional)
- Backend: Python + FastAPI
- YouTube Transcript: `youtube-transcript-api` (primary) and/or `pytube`/`yt-dlp` + speech-to-text fallback (Phase 1 optional; Phase 2 should handle “no subtitles available” cleanly)
- Token Counting: `tiktoken` (or provider-specific tokenizer)
- LLM: Provider API via a thin abstraction (OpenRouter)
- Dev/Runtime: CORS middleware, environment variables via `.env`

---

## High-Level System Architecture / Data Flow

### Components
1. **React UI**
   - Input: YouTube URL
   - Calls backend API
   - Renders:
     - Loading/working state
     - Summary result
     - Friendly error messages

2. **FastAPI Backend**
   - Endpoint: `POST /api/summarize`
   - Steps:
     1. Validate YouTube URL format and extract video ID
     2. Retrieve transcript (subtitles) for video ID
     3. If transcript unavailable:
        - Return structured error (Phase 2)
        - (Optional later) fallback to transcription from audio
     4. Call LLM with transcript and summarization instructions
     5. Return structured response:
        - summary text
        - metadata (video id/title, transcript length, provider used, etc.)

3. **LLM Provider Adapter (internal)**
   - Interface like `summarize(transcript: str, options: ...) -> SummaryResult`
   - Provider-specific implementation in Phase 3 (multiple providers)

### End-to-End Data Flow
1. User submits **YouTube URL** in React.
2. React sends **video URL** to `POST /api/summarize`.
3. FastAPI extracts **video ID** and fetches **transcript**.
4. FastAPI sends **transcript** to LLM.
5. FastAPI returns **summary** as JSON.
6. React displays the summary.

---

## Phase 1: Proof of Concept (POC)

### Objective
Validate feasibility of:
- Extracting transcripts from YouTube (or handling failures)
- Passing transcript to an LLM
- Producing a usable summary end-to-end

### Scope (strict)
- No complex UI
- No database
- No authentication
- A simple Python script/CLI only

### Suggested POC Tooling
- `youtube-transcript-api` for transcript retrieval
- A direct LLM call using one provider (single provider: OpenRouter)

### Deliverable (POC)
- A Python CLI that:
  - Accepts a YouTube URL
  - Fetches transcript
  - Calls LLM to summarize
  - Prints summary to stdout and exits non-zero on failure

---

### Sprint Plan (Phase 1)

#### Sprint P1.1 — Transcript Retrieval + Validation
**Tasks**
- [ ] Create `poc_summarize.py` (or `src/poc/poc_summarize.py`)
- [ ] Implement YouTube URL parsing to get `video_id`
- [ ] Implement transcript fetching using `youtube-transcript-api`
- [ ] Extract minimal video metadata (title/channel) using `yt-dlp` info-only mode (no media download)
- [ ] Implement error cases:
  - Invalid URL / cannot extract video ID
  - No subtitles available (explicit message)
  - Network/permission issues

**Definition of Done (DoD)**
- Running the CLI with a known video prints:
  - transcript fetched confirmation (at least transcript length)
  - or a clear, actionable error if subtitles are unavailable

#### Sprint P1.2 — LLM Summarization End-to-End
**Tasks**
- [ ] Implement LLM call (single provider) with:
  - System prompt: summarization instructions
- [ ] User prompt: transcript (plus extracted title/channel metadata)
- [ ] Add token-aware truncation/chunking policy using `tiktoken` (or provider tokenizer)
  - [ ] Count tokens for transcript
  - [ ] If tokens exceed model context budget, truncate by token budget (not by raw string length)
- [ ] Keep prompts JSON-safe (avoid slicing mid-UTF8/token boundaries)
- [ ] Print:
  - summary text
  - basic metadata (video id, transcript chars/words)

**Definition of Done (DoD)**
- CLI end-to-end works reliably for at least:
  - 1 video with subtitles
- Output is coherent and “summary-like” (meets human expectations for a first version)

---

## Phase 2: Minimum Viable Product (MVP) / Core Features

### Objective
Build a production-ready foundation:
- React web app with a simple input form and output display
- FastAPI backend API for summarization
- Robust error handling for invalid URLs and no subtitles available
- Basic CORS/API setup

### Scope (strict for MVP)
- No database persistence
- No user authentication
- One LLM provider for MVP
- Transcript-only summarization (fallback optional, but “no subtitles available” must be handled cleanly)

### Deliverables (MVP)
- Functional web app:
  - input form
  - loading state
  - summary output
  - error display (invalid URL, no subtitles)
- FastAPI backend:
  - `POST /api/summarize`
  - CORS configured for the frontend origin
  - structured JSON responses

---

### Sprint Plan (Phase 2)

#### Sprint P2.1 — Backend API Skeleton + Core Summarize Endpoint
**Tasks**
- [ ] Create FastAPI app with:
  - `POST /api/summarize` accepting JSON body: `{ "url": "<youtube_url>" }`
- [ ] Implement request validation:
  - extract video ID from URL
  - reject invalid URL with `400`
- [ ] Implement transcript retrieval:
  - if transcript unavailable: return `422` or `404` with message `NO_SUBTITLES_AVAILABLE`
- [ ] Implement LLM summarization:
  - apply same prompt/instruction pattern from Phase 1
- [ ] Implement token-aware truncation/chunking consistently using `tiktoken`
- [ ] Include extracted title/channel metadata in the LLM context
- [ ] Define response schema:
  - `summary: string`
  - `video_id: string`
  - `provider: string`
  - `transcript_summary_stats` (e.g., word count)

**Definition of Done (DoD)**
- Calling the endpoint with:
  - valid URL returns summary JSON
  - invalid URL returns a structured error
  - subtitles missing returns a structured “no subtitles” error

#### Sprint P2.2 — React Frontend (Form + Loading + Output/Error)
**Tasks**
- [ ] Build React page/component:
  - URL input field
  - Submit button
  - Loading indicator while waiting
  - Summary display component
  - Error banner component for structured errors
- [ ] Integrate with backend:
  - `fetch`/`axios` to `POST /api/summarize`
- [ ] Handle UX edge cases:
  - disable submit while loading
  - clear previous errors on new submit
  - show user-friendly error messages

**Definition of Done (DoD)**
- Manual testing from the browser:
  - Submits a URL and receives summary
  - Shows correct message for invalid URLs
  - Shows correct message for “no subtitles available”

#### Sprint P2.3 — CORS/API Setup + Basic Operational Hardening
**Tasks**
- [ ] Configure CORS in FastAPI for dev origin (and production-ready env var)
- [ ] Add environment variable handling:
  - LLM API key via `.env` (never commit secrets)
  - backend base URL for frontend (if needed)
- [ ] Add minimal logging:
  - request start/end
  - transcript fetch outcomes
  - LLM call latency (without logging transcript content)
- [ ] Add health endpoint:
  - `GET /health`

**Definition of Done (DoD)**
- Frontend successfully calls backend with CORS enabled
- Health endpoint returns expected status
- Logs show enough observability for debugging without leaking secrets

---

## Phase 3: Enhancements & Backlog (“Nice-to-haves”)

### Objective
Add enterprise-level features:
- User authentication
- Saving summary history in a database
- Let users select different AI providers
- UI/UX polishing

### Scope (Phase 3)
- Authentication + authorization
- Database persistence
- Provider selection (multi-provider LLM abstraction)
- UI enhancements (history view, provider selector, polished loading states)
- Performance and scalability improvements as needed

### Deliverables (Phase 3)
- Authentication
- Database-backed summary history (per user)
- Provider selection in UI + backend
- Improved UX and robustness

---

### Sprint Plan (Phase 3)

#### Sprint P3.1 — Authentication (Login/Session) + Protected History API
**Tasks**
- [ ] Implement auth mechanism (e.g., JWT or session cookies)
- [ ] Add auth-protected endpoint(s):
  - `GET /api/history`
  - `POST /api/summarize` (optionally protected, depending on product decision)
- [ ] Update frontend:
  - login UI (or “sign-in” button)
  - guard routes or show sign-in prompt before history access

**Definition of Done (DoD)**
- Unauthorized requests to protected endpoints return `401/403`
- Authorized users can access history API (even if history is seeded later)

#### Sprint P3.2 — Database + Summary Persistence (History)
**Tasks**
- [ ] Choose and implement database:
  - e.g., PostgreSQL + SQLAlchemy (or similar)
- [ ] Create schema:
  - `users`
  - `summaries` (fields: user_id, video_id, url, transcript stats, provider, summary text, created_at)
- [ ] On summarization:
  - persist summary result to database tied to user
- [ ] Implement history retrieval:
  - return list of recent summaries with metadata

**Definition of Done (DoD)**
- Summaries created in the app appear in user history
- History endpoint returns correct records filtered by user

#### Sprint P3.3 — AI Provider Selection + Backend Abstraction
**Tasks**
- [ ] Define internal interface for summarization provider(s)
- [ ] Implement provider adapter(s):
  - at minimum keep existing provider from Phase 2
  - add at least one additional provider (if feasible)
- [ ] Implement API fallback mechanism (enterprise resilience):
  - [ ] Configure primary provider + fallback provider(s) via env
  - [ ] On transient errors (e.g., HTTP 429/502/503/timeouts), automatically retry using fallback
  - [ ] Preserve request intent (same transcript + prompt + options) across providers
- [ ] Update API contract:
  - allow optional request field: `{ "provider": "openai" | "anthropic" | ... }`
- [ ] Update frontend:
  - provider selector in UI
  - show selected provider in metadata

**Definition of Done (DoD)**
- User selects provider and receives summary from that provider
- Backend responds with provider metadata
- Unsupported provider returns structured error `400`

#### Sprint P3.4 — UI/UX Polishing + Reliability Enhancements
**Tasks**
- [ ] UI improvements:
  - nicer loading states (progress/time estimates optional)
  - better error messages with actionable steps
  - summary formatting improvements (sections, bullet points)
- [ ] Reliability:
  - consistent truncation/chunking strategy across providers
  - add request timeouts and graceful failure messages
- [ ] Optional: rate limiting / abuse prevention (lightweight)

**Definition of Done (DoD)**
- End-to-end user experience feels production-grade:
  - smooth loading
  - correct errors
  - high perceived reliability
- No obvious client/backend mismatch in request/response schema

---

## System-Level Definition of Done (by Phase)

### Phase 1 DoD
- A single CLI/script demonstrates:
  - transcript extraction from YouTube
  - successful LLM call using transcript
  - readable summary output
  - correct failure messaging when transcript unavailable

### Phase 2 DoD
- Deployed locally (dev) a complete web app:
  - React form submits URLs
  - backend returns summary
  - invalid input and missing subtitles are handled with clear errors
  - CORS configured correctly
- Backend returns consistent JSON structures and appropriate HTTP codes

### Phase 3 DoD
- Production-ready enterprise features:
  - users can authenticate
  - summaries are persisted and retrievable in history
  - users can choose AI providers
  - UI is polished with robust handling and improved presentation

---

## Implementation Notes (Enterprise Agile, No Over-Engineering Early)
- Use YAGNI in Phase 1/2:
  - keep data model minimal (no DB until Phase 3)
  - keep provider abstraction simple (single provider first, extend later)
- Maintain clear contracts between frontend and backend:
  - request/response schemas defined early in Phase 2
- Ensure consistent error semantics:
  - frontend maps backend error codes to user-friendly messages

---

## Proposed Repository Structure (High-Level)
- `frontend/` (React app)
- `backend/` (FastAPI app)
- `poc/` (Phase 1 CLI/script)
- `docs/` (optional: runbooks, API docs)

---

## Verification / Acceptance Criteria (Cross-Phase)
- Transcript retrieval:
  - Works for videos with subtitles
  - Fails gracefully for videos without subtitles
- Summarization:
  - Produces coherent summary output
  - Respects token limits via truncation/chunking policy
- API stability:
  - Stable JSON schema and HTTP status codes
- Frontend correctness:
  - Proper loading state
  - Correct rendering of summary and errors
