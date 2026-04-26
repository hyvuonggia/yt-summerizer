# Task TSK-0305 — Users Table

**Task ID:** TSK-0305  
**Sprint:** P3.2 — Database + Summary Persistence (History)  
**Status:** pending

---

## Description

Create users table schema:
- id (UUID/INT)
- email (unique)
- password_hash
- created_at

---

## Acceptance Criteria

- [ ] Users table created
- [ ] Email unique constraint
- [ ] Password stored hashed

---

## Deliverables

- Model: User (SQLAlchemy)
- Table: `users`