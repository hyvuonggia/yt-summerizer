# Task TSK-0319 — Rate Limiting (Optional)

**Task ID:** TSK-0319  
**Sprint:** P3.4 — UI/UX Polishing + Reliability Enhancements  
**Status:** pending

---

## Description

Optional: lightweight rate limiting:
- Per-user rate limits
- Simple in-memory or Redis
- Return 429 when exceeded
- Headers: X-RateLimit-Remaining

---

## Acceptance Criteria

- [ ] Rate limit configured
- [ ] Returns 429 when exceeded
- [ ] Headers included

---

## Deliverables

- Middleware: rate limiter
- Config: RATE_LIMIT_PER_USER