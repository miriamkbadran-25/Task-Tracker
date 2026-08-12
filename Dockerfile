# syntax=docker/dockerfile:1

# ---- Build stage: install Python dependencies ----
FROM python:3.11-slim AS builder

WORKDIR /app

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

COPY backend/requirements.txt .
RUN pip install --user -r requirements.txt

# ---- Runtime stage: minimal image with only what's needed to run ----
FROM python:3.11-slim

# Create a non-root user to run the app
RUN useradd --create-home --shell /usr/sbin/nologin app

WORKDIR /app

# Bring in installed Python packages from the build stage
COPY --chown=app:app --from=builder /root/.local /home/app/.local

# Application code only (no tests, no venvs, no build tooling)
COPY --chown=app:app backend/app ./app
COPY --chown=app:app frontend /frontend

ENV PATH=/home/app/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
