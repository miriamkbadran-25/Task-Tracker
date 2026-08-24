# Module 5 Governance Retrospective

## What I Shared with AI Coding Tools

- Project rules: tech stack, run commands, task rules, and a rule not to share secrets or personal data.
- Project files: the FastAPI backend, simple frontend, Docker configuration, CI workflow, tests, and security notes.
- Example Kanban-board data, including the placeholder assignee names "Alice" and "Bob."
- Basic local context, such as the project folder and operating system. No secrets were viewed or shared.

## Risk Assessment

| Item shared | Risk | Reason | Safer future version | Ambiguity to resolve |
|---|---|---|---|---|
| Project rules: tech stack, run commands, task rules, and never sharing secrets or personal data. | Low | These are governance and setup details for a course toy project, with no sensitive data indicated. | "Python/FastAPI learning project; run and test commands; no secrets or personal data may be shared." | Confirm the rules do not contain internal URLs, account names, or credentials. |
| Project files: FastAPI backend, simple frontend, Docker, CI, tests, and security notes. | Low | The repository is described as a learning project and no proprietary logic, secrets, or real user data were identified. | Paste only the relevant file, minimal failing test, or sanitized diff needed for the question. | Confirm the repository is course/public code and contains no unreviewed secrets or third-party confidential code. |
| Example Kanban-board data, including placeholder names "Alice" and "Bob." | Low | The names are identified as placeholders rather than real user or customer data. | "Assignee A" and "Assignee B," with generic task titles and descriptions. | Confirm "Alice" and "Bob" are fictional placeholders, not real people. |
| Basic local context, such as the project folder and operating system. No secrets were viewed or shared. | Medium | Absolute paths and operating-system details can reveal a local username, machine structure, or internal environment context even without credentials. | "Windows development environment; local project directory omitted." | Whether the shared path included a real name, company identifier, network location, or other identifying information. |
