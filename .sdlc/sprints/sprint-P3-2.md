# Sprint P3.2 — Database + Summary Persistence (History)

**Phase:** Phase 3: Enhancements  
**Status:** pending  
**Sprint Goal:** Implement database with schema for users and summaries; persist summaries on creation; retrieve history.

---

## Tasks

| Task ID | Description | Status |
|--------|-------------|--------|
| [TSK-0304](TSK-0304-sprint-p3-2-database-schema.md) | Choose and implement database (PostgreSQL/SQLAlchemy) | pending |
| [TSK-0305](TSK-0305-sprint-p3-2-users-table.md) | Create users table schema | pending |
| [TSK-0306](TSK-0306-sprint-p3-2-summaries-table.md) | Create summaries table (user_id, video_id, url, transcript_stats, provider, summary_text, created_at) | pending |
| [TSK-0307](TSK-0307-sprint-p3-2-persist-summary.md) | On summarization, persist summary to database | pending |
| [TSK-0308](TSK-0308-sprint-p3-2-history-retrieval.md) | Implement history retrieval endpoint | pending |

---

## Definition of Done

- [ ] Summaries created in app appear in user history
- [ ] History endpoint returns records filtered by user

---

## Dependencies

- **Required:** Sprint P3.1 (authentication for user association)
- **Required:** Sprint P2.3 (base API stable)

---

## Exit Criteria

- [ ] Database schema created with users and summaries tables
- [ ] POST /api/summarize persists result to database
- [ ] GET /api/history returns user's summaries