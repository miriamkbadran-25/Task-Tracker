# Module 3 Kanban Board - Behavior Contract

**Purpose**: Define expected behaviors for testing before refactoring.  
**Date**: 2026-07-25  
**Scope**: Frontend Kanban board interactions, task management modals, drag-and-drop, error handling

---

## Behavior Contract Table

| ID | Behavior | How to Check Manually | Pass/Fail Notes |
|---|---|---|---|
| B1 | Three status columns render with correct counts | 1. Start the app with backend running<br>2. Observe the board loads with "To Do", "In Progress", "Done" columns<br>3. Verify each column header displays the task count in parentheses<br>4. Manually count tasks in each column and confirm counts match | ✓ Pass / ✗ Fail |
| B2 | Cards sort by priority inside each column | 1. Load the board<br>2. Inspect a column with 3+ tasks<br>3. Verify tasks are ordered from High → Medium → Low priority (or numbered 1, 2, 3)<br>4. Add a new high-priority task; confirm it moves to the top of its column | ✓ Pass / ✗ Fail |
| B3 | Loading state appears before tasks load | 1. Open browser DevTools Network tab and throttle to "Slow 3G"<br>2. Refresh the page<br>3. Verify a loading spinner/skeleton/message appears before tasks populate<br>4. Confirm loading state disappears once data arrives | ✓ Pass / ✗ Fail |
| B4 | Empty columns remain visible | 1. Load the board<br>2. If a column has no tasks, verify it still renders with the column header and "empty" state (e.g., "No tasks" message or visual)<br>3. Empty columns should not collapse or hide | ✓ Pass / ✗ Fail |
| B5 | Error state appears when backend is stopped | 1. Start the app and verify it loads normally<br>2. Stop the backend server (Ctrl+C in the terminal)<br>3. Refresh the page or wait for auto-refresh attempt<br>4. Verify an error message appears (e.g., "Failed to load tasks", "Connection refused")<br>5. Board should not render empty; error message should be visible | ✓ Pass / ✗ Fail |
| B6 | Valid drag sends PATCH and update the board | 1. Open browser DevTools Network tab<br>2. Drag a task from one column to another (e.g., To Do → In Progress)<br>3. Verify a PATCH request is sent to `/tasks/{taskId}` with the new status<br>4. Confirm the task moves visually on the board immediately (optimistic update) or after response<br>5. Verify counts in both columns update correctly | ✓ Pass / ✗ Fail |
| B7 | Invalid drag or server 422 reverts with message | 1. Temporarily modify backend to return 422 for a PATCH request (or use DevTools to simulate)<br>2. Drag a task to a new column<br>3. Verify the task reverts to its original column within 1 second<br>4. Confirm a toast/alert displays the server error message (e.g., "Cannot move task: Invalid status")<br>5. Board state remains consistent | ✓ Pass / ✗ Fail |
| B8 | New Task and Edit modal flows work with validation | **New Task:**<br>1. Click "New Task" button<br>2. Modal opens with title input field (empty)<br>3. Attempt to submit without entering a title; verify validation error appears (e.g., red border, "Title required")<br>4. Enter a valid title; submit<br>5. Verify new task appears on the board in "To Do" column<br>6. Click outside modal or press Escape; verify modal closes<br><br>**Edit Task:**<br>7. Click edit icon on an existing task<br>8. Modal opens with current title pre-filled<br>9. Clear the title; attempt to submit; verify validation error<br>10. Modify the title; submit<br>11. Verify task updates on the board<br>12. Test modal dismissal (close button, Escape, click outside) | ✓ Pass / ✗ Fail |

---

## Testing Notes

- **Prerequisites**: Backend must be running on `http://127.0.0.1:8000` for tests B1-B4, B6, B8
- **B5 Testing**: Stop backend intentionally; restart after test completes
- **B6 & B7**: Use browser DevTools → Network tab to monitor HTTP requests
- **B8 Validation**: Test both empty submission and characters-only submission (if applicable)
- **Regression Check**: After each behavior passes, verify it doesn't break previous passing behaviors

---

## Sign-Off

| Role | Name | Date | Status |
|---|---|---|---|
| Tester | — | — | ☐ Reviewed |
| Developer | — | — | ☐ Approved |
