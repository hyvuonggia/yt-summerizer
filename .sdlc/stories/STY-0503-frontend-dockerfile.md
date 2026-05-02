# STY-0503: Frontend Dockerfile

**Epic:** EPIC-0501 | **Requirement:** REQ-0501 | **Priority:** P1 | **Estimate:** 2
**Status:** Ready | **Owner:** CoderAgent | **Sprint:** -

## User Story
As a developer, I want the Frontend to run in a Docker container, so that it has a consistent environment.

## Acceptance Criteria
- [ ] Dockerfile created for Frontend
- [ ] Node dependencies installed
- [ ] Application runs on port 3000
- [ ] Built with production build for smaller image
- [ ] Nginx serves the static files

## Definition of Ready (DoR)
- [x] Description clear and unambiguous
- [x] Acceptance criteria written in Given/When/Then
- [x] Dependencies identified (none)
- [x] Estimate agreed (2 points)
- [x] Non-functional requirements captured

## Definition of Done (DoD)
- [ ] Dockerfile created in frontend/ directory
- [ ] nginx.conf created for serving static files
- [ ] .dockerignore created
- [ ] Tested with docker compose

## Linked Tasks
- TSK-0503

## Execution Log
- *[2026-05-02 13:35]* Created by ProductOwner