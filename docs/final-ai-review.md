# Final AI Review and Ownership Evidence
## AGENTS.md guardrails
- Repo-specific stack and commands included: yes
- Docs-first/read-first guardrail included: yes
- Unexpected app/frontend edits rule included: yes
## AI code review mini-log
| AI comment | Grade: Useful / Noise / Wrong | Reason | Verification or decision |
|---|---|---|---|
| `GET /tasks` does not expose the status/priority filters that storage supports. | Useful | `backend/app/main.py` calls `storage.get_all_tasks()` without query parameters, while `backend/app/storage.py` accepts filters. | Recorded as a limitation; no feature was added because final-project scope forbids new product features. |
| An unchanged status is always rejected by the transition rule. | Wrong | The route only validates a supplied status when it differs from the stored status. | Checked `backend/app/main.py` and the passing `test_task_update_priority_and_status`; documentation states the unchanged-status exception. |
| Move the empty routes/services/schema modules into a new service layer. | Noise | The files are unused, but a refactor does not address a release defect and would expand final-project scope. | Rejected; retained the existing application structure. |
## AI security mini-review
| Finding | File evidence | Grade: Valid / False Positive / Noise | Reason | Next action |
|---|---|---|---|---|
| No authentication or task ownership checks. | `backend/app/main.py`, `README.md` current limitations | Valid | Anyone reaching a future public deployment could operate on any task. The course app deliberately has no authentication. | Keep it documented as a production blocker; define an authentication/authorization model before public deployment. |
| Unbounded in-memory task collection and full-list response. | `backend/app/storage.py`, `backend/app/models.py`, `backend/app/main.py` | Valid | Tasks are held in a module-level dictionary, descriptions/assignees have no length limits, and the list route returns every task. | Define size limits, pagination, and persistence/retention requirements before production use. |
| Broad CORS is an immediate vulnerability in this local course app. | `backend/app/main.py` | Noise | The permissive configuration is real, but no authentication, cookies, or cross-origin deployment are implemented; calling it an immediate exploitable vulnerability would overstate the evidence. | Reassess CORS when an authenticated or hosted deployment is introduced. |
## Manual security check
I manually checked the Docker runtime instructions and image configuration: `Dockerfile` creates and switches to the unprivileged `app` user, and `.dockerignore` excludes `.env` and `.env.*`. The recorded image inspection in `docs/release-evidence.md` confirms the image user is `app`. This matters because the container has an explicit least-privilege runtime setting and does not send common environment files in its build context.
## One AI output I rejected or corrected
An AI review treated dependency-advisory claims as confirmed security findings. I rejected that conclusion because the review did not establish the affected version range, whether the dependency is reachable in the runtime image, or a realistic attack path. I kept those claims unconfirmed in `docs/security-review.md` and only recorded code-visible findings with file evidence.
## Three AI usage rules
1. Never paste: credentials, tokens, `.env` values, private data, or production logs into an AI tool.
2. Always verify: AI claims against the repository, a diff review, and an appropriate test or runtime command before accepting them.
3. Record AI contributions by: keeping short evidence notes that state the suggestion, the file/command checked, and the final human decision.
## Ownership statement
I understand the application’s FastAPI routes, in-memory storage, validation rules, frontend boundary, CI workflow, and Docker runtime choices. I reviewed the documentation and configuration changes against the repository and kept final-project work within the existing course scope. I treated AI output as suggestions, grading useful findings and rejecting unsupported ones rather than accepting them automatically. The recorded tests, Docker health check, CI run, and remaining limitations give me evidence for the claims I make in this submission.
