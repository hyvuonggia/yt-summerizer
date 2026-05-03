# TSK-0601: Remove Authentication and Database
**Story:** STY-0601 | **Sprint:** sprint-P6-1 | **Status:** Done
**Assignee:** - | **Estimate:** 5

## Description
Remove authentication (JWT/bcrypt) and database (MySQL) from the application, reverting to open-access mode. This is a rollback/reversion request from the user.

### Backend Changes Required
- [ ] Remove `/api/auth/register` endpoint from `main.py`
- [ ] Remove `/api/auth/login` endpoint from `main.py`
- [ ] Remove `/api/history` endpoint from `main.py`
- [ ] Remove `/api/history/{id}` endpoint from `main.py`
- [ ] Remove `get_current_user` dependency from `main.py`
- [ ] Remove auth imports from `main.py`
- [ ] Remove database initialization from `main.py` (`init_db`, `close_db`)
- [ ] Update `/api/summarize` endpoint to remove auth requirement (open to all)
- [ ] Remove auth-related models from `models.py` (UserCreate, UserLogin, Token)
- [ ] Delete `backend/services/auth.py` entirely
- [ ] Delete `backend/database.py` entirely
- [ ] Remove database config from `config.py` (DB_HOST, DB_PORT, DB_USER, etc.)

### Frontend Changes Required
- [ ] Remove auth API functions from `api.ts` (registerUser, loginUser, logoutUser, getStoredToken, storeToken, etc.)
- [ ] Remove token requirements from summarizeUrl, getUserHistory, deleteHistoryItem
- [ ] Delete `components/LoginForm.tsx`
- [ ] Delete `components/ProtectedRoute.tsx`
- [ ] Delete `AuthContext.tsx`
- [ ] Remove AuthProvider from `App.tsx`
- [ ] Remove protected routes - make home page public

### Docker Changes Required
- [ ] Remove MySQL service from `docker-compose.yml`
- [ ] Remove database environment variables from backend service
- [ ] Remove JWT environment variables from backend service
- [ ] Remove mysql volume
- [ ] Remove mysql from backend depends_on

### Test Files to Review
- [ ] Check `test_database_auth.py` - likely obsolete, review for removal/update

## Acceptance Criteria
- [ ] Backend starts without database connection errors
- [ ] `/api/summarize` endpoint works without auth token
- [ ] Frontend home page loads without login requirement
- [ ] Docker compose starts only backend + frontend (no MySQL)
- [ ] Application functions as basic YouTube summarizer (no user accounts)

## Dependencies
- None - this is a rollback operation

## Execution Log
- *[2026-05-03]* Task ticket created by Engineering Manager
- *[2026-05-03]* Linked to STY-0601 and sprint-P6-1
- *[2026-05-03]* PM approved sprint commitment - starting execution
- *[2026-05-03]* Backend: removed auth endpoints, database, config (main.py, models.py, config.py)
- *[2026-05-03]* Backend: deleted services/auth.py, database.py
- *[2026-05-03]* Frontend: removed auth API, components (api.ts, AuthContext, LoginForm, ProtectedRoute, HistoryDisplay)
- *[2026-05-03]* Frontend: updated App.tsx, Header.tsx
- *[2026-05-03]* Docker: removed MySQL service from docker-compose.yml
- *[2026-05-03]* Build verified: frontend builds successfully
- *[2026-05-03]* Task completed - all auth/database removed