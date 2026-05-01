# Task TSK-0301 — Auth Mechanism

**Task ID:** TSK-0301  
**Sprint:** P3.1 — Authentication (Login/Session) + Protected History API  
**Status:** ✅ done

---

## Description

Implement authentication mechanism:
- JWT tokens or session cookies
- Password hashing (bcrypt or similar)
- Login/signup endpoints

---

## Acceptance Criteria

- [x] User can register/login
- [x] JWT or session created
- [x] Passwords hashed

---

## Deliverables

- Auth service in `backend/services/auth.py`
- Models: User, Token

---

## Execution Log
- *[2026-05-01 20:20]* Auth mechanism implemented - JWT tokens, bcrypt password hashing, register/login endpoints
- *[2026-05-01 20:20]* Tested and verified working