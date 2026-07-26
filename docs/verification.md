# Verification Report

Date: 2026-07-27
Scope: Backend and frontend verification for the task tracker Kanban flow and refactor regression checks.

## 1. Baseline Check

### Setup verified
- Started the backend with: `uvicorn app.main:app --reload --port 8000`
- Confirmed the app was reachable at `http://127.0.0.1:8000/`
- Verified that the root page rendered the Task Tracker UI instead of failing with a server error.

### Baseline outcome
- The board loaded successfully in the browser.
- The page displayed the expected Kanban structure with three columns: To Do, In Progress, and Done.
- The backend test baseline was not fully green: the suite showed 2 failing tests and 28 passing tests.

## 2. Backend Test Results

### Command run
```bash
cd /d c:\Users\miria\task-tracker\backend && python -m pytest -q
```

### Result
- 28 tests passed
- 2 tests failed
- Overall status: not yet fully green

### Notable failures
- `test_create_task_valid_returns_201_with_full_body`
- `test_patch_same_status_returns_422`

## 3. Manual Browser Checks

### Checks performed
- Opened `http://127.0.0.1:8000/` in the browser.
- Confirmed the page title and heading were present.
- Verified the board rendered with visible columns and task cards.
- Observed a loading state (`Loading tasks...⏳`) before the board content became visible.

### Observed UI behavior
- The page rendered the expected Kanban board shell.
- Three columns were visible with populated task cards.
- The interface exposed actions such as the New Task button and task edit controls.

## 4. Behavior Contract: Before vs. After Refactor

| Contract area | Before refactor | After refactor (target) |
|---|---|---|
| Board loads with three columns | Observed in browser: To Do, In Progress, and Done were present | Re-check after fixes; expected to remain intact |
| Task cards render in columns | Observed with sample tasks visible in the UI | Re-check after fixes; expected to remain intact |
| Loading state appears before content | Observed during the browser check | Expected to remain intact |
| Empty columns remain visible | Not explicitly exercised in this session | Re-check after fixes |
| Error state when backend is stopped | Not explicitly exercised in this session | Re-check after fixes |
| Drag/drop updates task status | Not exercised in this session | Re-check after fixes |
| Invalid drag reverts with error feedback | Not exercised in this session | Re-check after fixes |
| New/edit modal validation works | Not exercised in this session | Re-check after fixes |

## 5. Break Test Evidence

### Break test 1: tag normalization regression
- Test: `test_create_task_valid_returns_201_with_full_body`
- Expected: tags should be stored exactly as provided, e.g. `['urgent', 'backend']`
- Actual: response returned `['Urgent', 'Backend']`
- Evidence from pytest:

```text
E AssertionError: assert ['Urgent', 'Backend'] == ['urgent', 'backend']
```

### Break test 2: same-status patch regression
- Test: `test_patch_same_status_returns_422`
- Expected: patching a task to the same status should be rejected with `422`
- Actual: the request returned `200 OK`
- Evidence from pytest:

```text
E assert 200 == 422
```

## 6. Summary

The current verification baseline shows that the app can load and render the Kanban board, but the backend regression suite is not yet fully passing. The two reported break tests are concrete examples of behavior that should be corrected before the refactor is considered complete.
