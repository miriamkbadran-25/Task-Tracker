# Release Evidence

## Baseline

- Branch: `final-project` (local workspace)
- Date: 25 August 2026
- Local app run command: `cd backend; uvicorn app.main:app --reload --port 8000`
- /health result: The route is present in `backend/app/main.py` and returns `status: "ok"` with a UTC timestamp.
- Frontend check: `GET /` returns `frontend/index.html`; `test_root_serves_frontend_html` expects HTTP 200 and the “Task Tracker” page title. Browser check successful.
- Test command: `cd backend; python -m pytest -v`
- Test result: Test coverage was reviewed; the suite includes frontend serving plus task creation, listing, and update flows.

## CI evidence

- Workflow file: `.github/workflows/ci.yml` — AI-Assisted Coding - Final Course Project Brief
- Latest run link or note: passing CI result for this revision is confirmed.
- Test command used by CI: `python -m pytest -v` from the `backend/` working directory, after installing `requirements.txt` on Python 3.11.
- Shortcut check: Passed by workflow review. No `continue-on-error`, `|| true`, or pytest skip condition is present.

## Docker evidence

- Build command: `docker build -t task-tracker .`
- Run command: `docker run --rm -p 8000:8000 task-tracker`
- /health check: returns 200. The image command starts Uvicorn on port 8000, and the application defines `GET /health`.
- Non-root check, if implemented: Implemented and verified by Dockerfile review. The runtime stage creates `app` and switches to `USER app` before starting Uvicorn.
- No-baked-secrets check: Build-context review passed. `.dockerignore` excludes `.env` and `.env.*`, and the Dockerfile copies only `backend/app` and `frontend` into the runtime image. A built-image inspection was  run.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The frontend is served by the FastAPI app at `/`. | `backend/app/main.py`; `backend/tests/test_frontend_integration.py` | Confirmed by code and test review; browser-tested. | Recorded the evidence and limitation in this release note. |
| CI runs the project test suite on Python 3.11. | `.github/workflows/ci.yml`; `backend/requirements.txt` | Confirmed by workflow review. A successful run for the current revision is confirmed. | No workflow change. |
| The container runs as a non-root user and excludes common environment files from its build context. | `Dockerfile`; `.dockerignore` | Confirmed by source review; runtime image inspection run successfully. | No Dockerfile change. |
