# STY-0402: Backend Progress Updates

**Epic:** N/A | **Priority:** P1 | **Estimate:** 3 pts
**Status:** Backlog | **Owner:** ProductOwner | **Sprint:** -

## User Story
As a user, I want to see progress updates from the backend during the summarization process, so that I know what's happening and don't think the application is stuck.

## Acceptance Criteria
- [ ] Given the user submits a YouTube URL, When the backend is processing (fetching transcript, calling LLM), Then the backend should log progress messages to show what's happening
- [ ] Given the LLM is generating the summary, When the response is received, Then the backend should log that the response is received and being processed
- [ ] Given the summary is ready and sent to frontend, When the response is returned, Then the backend should log the completion with processing time

## Current Behavior (Problem)
- Backend shows: `INFO: 127.0.0.1:48354 - "POST /api/summarize HTTP/1.1" 200 OK`
- Then: `Waiting for LLM response... (38s)` (printed to console)
- No further logs until response is complete
- User has no visibility into what's happening

## Expected Behavior
- Backend should log each stage:
  - "Fetching transcript..."
  - "Transcript fetched, X words"
  - "Calling LLM..."
  - "LLM response received, Y tokens"
  - "Sending response to client..."

## Technical Notes
- Current implementation in `backend/services/summarization.py` has a progress counter but only prints to console
- Need to add proper logging at each stage in `backend/main.py`
- Consider using structured logging with different levels (INFO for progress, DEBUG for details)

## Dependencies
- None (backend-only change)

## Definition of Ready (DoR)
- [x] Description clear and unambiguous
- [x] Acceptance criteria written in Given/When/Then
- [x] Dependencies identified (or none)
- [x] Estimate agreed (3 pts)
- [ ] Non-functional requirements captured (perf, security, a11y)

## Definition of Done (DoD)
- [ ] Code implemented and merged
- [ ] Unit + integration tests passing
- [ ] Delta coverage on new/modified code ≥ 80%
- [ ] Code reviewed by CodeReviewer (no blocking findings)
- [ ] Build green (BuildAgent) and CI green (DevOpsAgent)
- [ ] Documentation updated (DocWriter)
- [ ] Acceptance verified by ProductOwner
- [ ] No P0/P1 defects open

## Linked Tasks
- TSK-0404: Add progress logging in backend main.py
- TSK-0405: Improve logging in summarization service

## Execution Log
- *2026-04-29 21:55* Created by ProductOwner - Added to backlog from new requirements