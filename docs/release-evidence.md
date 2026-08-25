# Release Evidence

## Baseline

- Branch: `final-project` (local workspace)
- Date: 25 August 2026
- Local app run command: `cd backend; uvicorn app.main:app --reload --port 8000` (not run directly; the same app was verified through Docker Compose).
- /health result: `docker compose up --build --detach --wait` reported the service `healthy`; `GET http://127.0.0.1:8000/health` returned HTTP 200 with `{"status":"ok", ...}`. The verification stack was removed with `docker compose down`.
- Frontend check: `test_root_serves_frontend_html` passed, confirming that `GET /` serves the expected HTML. A browser check of the Kanban board and create/edit flow is **not confirmed** in this evidence record.
- Test command: `cd backend; .\\.venv\\Scripts\\python.exe -m pytest -v`
- Test result: Python 3.11.9; all 3 tests passed. `python -m pip check` reported no broken requirements.

## CI evidence

- Workflow file: `.github/workflows/ci.yml` — AI-Assisted Coding - Final Course Project Brief
- Latest green run: [CI run #11 for `b1a9188`](https://github.com/miriamkbadran-25/Task-Tracker/actions/runs/32878067301) completed successfully on 25 August 2026.
- Test command used by CI: `python -m pytest -v` from the `backend/` working directory, after installing `requirements.txt` on Python 3.11.
- Shortcut check: Passed by workflow review. No `continue-on-error`, `|| true`, or pytest skip condition is present.

## Docker evidence

- Build/run command: `docker compose up --build --detach --wait`.
- Result: Docker Desktop 4.88.1 / Docker Engine 29.7.2 rebuilt `task-tracker-task-tracker`, started the service, and reported it healthy.
- /health check: Passed as described above.
- Non-root check: `docker image inspect` confirmed `User=app` and `ExposedPorts={"8000/tcp":{}}`.
- No-baked-secrets check: `.dockerignore` excludes `.env` and `.env.*`, and the Dockerfile copies only `backend/app` and `frontend` into the runtime image. This is a build-context/source review; image-layer secret scanning was not run.

## Documentation claim-vs-reality log

| Claim checked | Evidence used | Result | Change made, if any |
|---|---|---|---|
| The frontend is served by the FastAPI app at `/`. | `backend/app/main.py`; `backend/tests/test_frontend_integration.py` | Confirmed by code and a passing automated test; browser interaction was not run. | Recorded the evidence and limitation in this release note. |
| CI is configured to run the project test suite on Python 3.11. | `.github/workflows/ci.yml`; `backend/requirements.txt` | Confirmed by workflow review. A successful run for the current revision was not independently verified. | No workflow change. |
| The container runs as a non-root user and excludes common environment files from its build context. | `Dockerfile`; `.dockerignore`; `docker image inspect` | Confirmed: the inspected image runs as `app`; build-context exclusions were reviewed. | No Dockerfile change. |
