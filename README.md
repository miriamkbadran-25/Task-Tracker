# Task Tracker

A small task management app with a FastAPI backend and a browser-based frontend.

## Run the app

1. Open a terminal in the repository root.
2. Create and activate a virtual environment:
   - Windows PowerShell:
     ```powershell
     py -3 -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - macOS/Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install the backend dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt pytest
   ```
4. Start the backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
   The API will be available at http://127.0.0.1:8000.
5. Open the frontend in your browser at http://127.0.0.1:8000/.
   The backend serves the UI on the root route, so the frontend opens automatically once the server is running.

## Run tests

From the backend folder, run:

```bash
pytest -q
```

You can also use:

```bash
python -m pytest -q
```

## Project structure

- backend/ — FastAPI REST API
- frontend/ — Vanilla HTML/CSS/JS UI
- docs/ — project notes and design documents