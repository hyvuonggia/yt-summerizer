# Task TSK-0214 — Environment Variables

**Task ID:** TSK-0214  
**Sprint:** P2.3 — CORS/API Setup + Basic Operational Hardening  
**Status:** pending

---

## Description

Add environment variable handling:
- LLM API key from .env (OPENROUTER_API_KEY)
- Frontend base URL for CORS (CORS_ORIGINS)
- LLM model (LLM_MODEL)
- Environment (dev/prod)

---

## Acceptance Criteria

- [ ] .env.example created
- [ ] Settings loaded in backend
- [ ] Never commit actual secrets

---

## Deliverables

- Config: `backend/config.py`
- .env.example with placeholder values