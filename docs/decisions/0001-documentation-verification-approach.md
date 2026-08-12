# Technical Decision Note – Documentation Verification Approach

**Status:** Draft

## 1. Context

The Module 4 Task Tracker is a FastAPI backend that uses Pydantic v2 with in-memory storage. The project is documented through Google-style docstrings in `app/main.py` and `app/models.py`, along with the `README.md`.

Initially, the documentation was written by reviewing the source code without running the application. Although this gave a good understanding of the API, it failed to uncover some runtime behavior. For example, `TaskUpdate` accepted explicit `null` values for fields such as `title`, and because updates were applied with `setattr()`, Pydantic validation was bypassed. As a result, the API could return invalid data even though the schema defined those fields as non-nullable. This issue only became apparent after testing the running application with real HTTP requests.

This decision focuses only on verifying documentation accuracy, not security, deployment, or production readiness.

## 2. Decision

Documentation should be based on verified runtime behavior rather than assumptions from reading the source code. Before documenting API behavior such as validation rules, HTTP status codes, or response formats, the application should be tested by sending real HTTP requests. If a behavior has not yet been confirmed, it should be marked with **[VERIFY]** instead of being presented as fact.

## 3. Alternatives Considered

* **Static code review only:** Rejected because it missed runtime issues that only appeared when the application was executed.
* **Relying only on the existing test suite:** Existing tests did not cover the null-value scenarios that exposed the validation issue.
* **Adding static type checking:** Not pursued because type checking would not detect this specific runtime behavior.

## 4. Trade-offs

Verifying documentation against a running application takes more time than simply reading the code and requires a working environment. In this project specifically, that meant testing through `Dockerfile`-built containers rather than a direct local `pytest`/`uvicorn` run, and because `storage.py` holds every task in a plain in-memory dict, state resets on every restart — each verification pass had to recreate its own test tasks from scratch instead of reusing fixtures from a prior run. However, it produces more accurate documentation and reduces the risk of documenting behavior that does not match the actual API. The additional effort is worthwhile, especially for documenting validation rules and API responses. I would do this differently by writing automated tests for the null-value cases at the same time as fixing them, instead of relying on manual verification and leaving that gap for later.

## 5. Consequences

* Live testing uncovered validation issues that were not obvious from the source code alone.
* Documentation now distinguishes between verified behavior and items that still require confirmation.
* The verification steps were performed manually and are not yet covered by automated tests, so future regressions could go unnoticed.
* Maintaining accurate documentation depends on consistently verifying changes against a running application.

## 6. Open Questions

* Should the manual verification steps be converted into automated tests?
* Should the CI pipeline be expanded to cover the validation behavior that was verified manually?
* Should the project adopt a documented verification process (for example, in a `CONTRIBUTING.md` or similar guide) so future documentation follows the same approach?

## README Link

This note will live at `docs/decisions/0001-documentation-verification-approach.md`. Once added, `README.md`'s "Related documents" section should link to it — that section currently references an "ADR-001" that does not exist anywhere in the repo, so this note can either replace that reference or sit alongside it.
