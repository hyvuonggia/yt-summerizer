# BUG-0001: ImportError - attempted relative import beyond top-level package
**Severity:** High | **Status:** Fixed
**Found In:** sprint-P2-4 | **Related:** STY-0401

## Steps to Reproduce
1. Start the FastAPI server: `python -m backend.main`
2. Send a POST request to `/api/summarize` with a valid YouTube URL
3. Server returns 500 Internal Server Error with ImportError

## Expected vs Actual
- **Expected:** Request processes normally, returns summary response
- **Actual:** 500 Internal Server Error with traceback showing:
  ```
  ImportError: attempted relative import beyond top-level package
  File "/home/hyvuonggia/projects/yt-summerizer/backend/main.py", line 199, in summarize_video
    from ..models import SUPPORTED_SUMMARY_LANGUAGES
  ```

## Root Cause Analysis
The import statement on line 199 of `backend/main.py` used incorrect relative import syntax:
```python
from ..models import SUPPORTED_SUMMARY_LANGUAGES
```

The `..` means "go up two package levels", but when running as a top-level module (e.g., `python -m backend.main`), there is no parent package above `backend`. This causes the ImportError.

All other imports in the same file correctly use single-dot relative imports (e.g., `from .models import ...`), making this an inconsistent typo.

## Fix Plan
- [x] Change `from ..models import` to `from .models import` on line 199
- [x] Verify fix by importing the module successfully

## Execution Log
- *2026-04-29* Found during runtime by user report
- *2026-04-29* Fixed import statement (changed `..models` to `.models`)
- *2026-04-29* Verified fix with `python -c "from backend.main import app"`