# Module 5 Security Review

## Reconciliation

| Agreement | AI-only | You-only |
|---|---|---|
| None. | SEC-01 — No authentication or ownership checks (Valid). | `python-dotenv==1.0.1` advisory claim — What business logic uses `set_key()` or `unset_key()`, if any? Is dotenv used only for local development, or will this package be present in a production runtime/image? What attacker-controlled path or environment-file write capability is in scope? **Needs evidence:** advisory affected-version range and patched version. |
|  | SEC-02 — Broad CORS configuration (Noise). | `pytest==7.4.2` advisory claim — Is pytest strictly CI/test-only, or can it run in a production/admin workflow? Does the project execute untrusted tests, plugins, or repository content in CI? Is the reported advisory applicable to `7.4.2`, given the supplied version mismatch? **Needs evidence:** authoritative advisory details and affected-version range. |
|  | SEC-03 — Unbounded in-memory task collection and unbounded fields (Valid). |  |
|  | SEC-04 — String coercion in validators (Noise). |  |
|  | SEC-05 — Hard-coded `http://localhost:8000` frontend API origin (Valid). |  |
|  | SEC-06 — Dependency/CI supply-chain hardening gaps (Noise). |  |

## Observation

AI coverage was strongest for code-visible architectural limits, including access control, resource growth, and frontend deployment configuration.
It missed dependency-advisory checks and the associated threat-model questions about reachable business logic, deployment scope, and attacker capability.

## Top-3 security backlog

| Rank | Finding | Why it matters | Suggested owner | Next action |
|---|---|---|---|---|
| 1 | SEC-01: No authentication or task ownership checks | If deployed where untrusted users can reach it, anyone can create, alter, or delete tasks. The repository explicitly documents this as a current limitation. | Backend / course-project owner | Record it as a production blocker; define the required authentication and authorization model before any public deployment. |
| 2 | SEC-03: Unbounded in-memory storage, fields, and list response | Request/task growth can consume process memory and make responses increasingly expensive. | Backend | Define task/field limits and pagination/retention expectations before production use. |
| 3 | SEC-05: Hard-coded localhost API base | In hosted use, the browser calls the visitor’s machine instead of the service that served the frontend. | Frontend | Use a same-origin/relative API base or environment-specific configuration; verify the deployed browser flow. |

## Evidence notes

- SEC-01 is supported by `README.md` (current limitations), `backend/app/main.py` (task routes without identity or ownership checks), and `Dockerfile` (Uvicorn bound to `0.0.0.0`). Public deployment is not configured or confirmed.
- SEC-03 is supported by `backend/app/models.py` (no length limits for `description` or `assignee`), `backend/app/storage.py` (module-level in-memory task dictionary), and `backend/app/main.py` (`GET /tasks` returns the full collection). No practical exhaustion threshold has been measured.
- SEC-05 is supported by `frontend/index.html` (absolute localhost API base), `backend/app/main.py` (serves the frontend), and `README.md` (combined frontend/backend setup).
- The two manual dependency findings are not included in the backlog because the referenced advisories and affected-version ranges require independent evidence before they can be treated as confirmed.
