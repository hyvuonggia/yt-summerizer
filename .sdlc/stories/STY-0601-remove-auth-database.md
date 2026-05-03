# STY-0601: Remove Authentication and Database
**Epic:** - | **Requirement:** - | **Priority:** P0 | **Estimate:** 5
**Status:** Done

## User Story
As a user,
I want to use the YouTube summarizer without creating an account,
So that I can quickly summarize videos without registration barriers.

## Acceptance Criteria
- [ ] Given an unauthenticated user, When they visit the home page, Then they see the summarize form immediately (no login redirect)
- [ ] Given a valid YouTube URL, When the user submits to /api/summarize, Then the summary is returned without requiring an auth token
- [ ] Given Docker Compose, When running `docker-compose up`, Then only backend and frontend services start (no MySQL)
- [ ] Given the backend, When starting, Then it starts without database connection errors

## Definition of Ready (DoR)
- [ ] Description clear and unambiguous
- [ ] Acceptance criteria written in Given/When/Then
- [ ] Dependencies identified (or none)
- [ ] Estimate agreed (story points)
- [ ] Non-functional requirements captured (perf, security, a11y)

## Definition of Done (DoD)
- [ ] Backend /api/summarize works without auth token
- [ ] Frontend home page is public (no ProtectedRoute wrapper)
- [ ] Docker compose has no MySQL service
- [ ] Backend starts without database errors
- [ ] Auth-related files removed from codebase
- [ ] Build passes
- [ ] No critical defects open

## Linked Tasks
- TSK-0601 (to be created)

## Execution Log
- *[2026-05-03]* Created by Engineering Manager - awaiting sprint planning