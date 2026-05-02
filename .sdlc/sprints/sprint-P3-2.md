# Sprint P3.2 — Database + Summary Persistence (History)

**Phase:** Phase 3: Enhancements  
**Status:** completed  
**Sprint Goal:** Implement database with schema for users and summaries; persist summaries on creation; retrieve history.

---

## Tasks

| Task ID | Description | Status |
|---------|-------------|--------|
| [TSK-0304](TSK-0304-sprint-p3-2-database-schema.md) | Choose and implement database (MySQL/SQLAlchemy) | completed |
| [TSK-0305](TSK-0305-sprint-p3-2-users-table.md) | Create users table schema | completed |
| [TSK-0306](TSK-0306-sprint-p3-2-summaries-table.md) | Create summaries table (user_id, video_id, url, transcript_stats, provider, summary_text, created_at) | completed |
| [TSK-0307](TSK-0307-sprint-p3-2-persist-summary.md) | On summarization, persist summary to database | completed |
| [TSK-0308](TSK-0308-sprint-p3-2-history-retrieval.md) | Implement history retrieval endpoint | completed |

---

## Definition of Done

- [x] Summaries created in app appear in user history
- [x] History endpoint returns records filtered by user

---

## Dependencies

- **Required:** Sprint P3.1 (authentication for user association)
- **Required:** Sprint P2.3 (base API stable)

---

## Exit Criteria

- [x] Database schema created with users and summaries tables
- [x] POST /api/summarize persists result to database
- [x] GET /api/history returns user's summaries

---

## Implementation Notes

- **Database:** MySQL 8 with SQLAlchemy async (aiomysql)
- **Password Hashing:** bcrypt (industry standard)
- **Tables:** `users` (id, email, username, hashed_password, created_at, updated_at), `summaries` (id, user_id, video_id, video_title, video_url, video_channel, transcript_language, transcript_word_count, transcript_duration, llm_provider, llm_model, summary_text, created_at)
- **Tested:** Registration with bcrypt password hashing, login with password verification, database persistence