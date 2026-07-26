# Task Tracker

A learning project implementing a simple REST API backend (FastAPI)
with a separate frontend, following a layered architecture with
in-memory storage.

## Status

This repository currently contains the **backend skeleton only**
(health check endpoint). CRUD functionality, task status rules, and
the frontend will be added in subsequent tasks.

## Architecture

See `ADR-001` (Use a Simple Layered FastAPI Architecture with
In-Memory Storage) for the full architecture decision, including:

- Layered structure: Routes → Service → Storage → In-memory data store
- Task model: title, description, status, priority, assignee
- Status transition rules (ToDo ↔ InProgress → Done, no reverse from Done)
- Explicit out-of-scope items: authentication, user accounts,
  multi-tenancy, real-time updates, mobile apps

## Structure
task-tracker/
├── backend/ # FastAPI REST API (see backend/README.md)
├── frontend/ # Vanilla HTML/CSS/JS (added later)
└── README.md

## Getting Started

See [`backend/README.md`](backend/README.md) for setup, run, and test
instructions.