# Task Tracker API — Backend

A FastAPI backend for the Task Tracker project.

## Quick start

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt pytest
   ```
3. Start the backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
4. Open the app in your browser at http://127.0.0.1:8000/.
   The backend serves the frontend on the root route.
5. View the API docs at http://127.0.0.1:8000/docs.

## Run tests

From the backend folder, run:

```bash
pytest -q
```

## Health check

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "ok"
}
```
