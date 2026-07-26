FEATURE: DUE DATE

US-1	As a team member, I want to create a task with an optional due date so that I can keep track of when work should be completed.	1. A task can be created with or without a due date.
- The due date must be today or a future date; selecting a past date is rejected with a validation error.
- A valid due date is stored and returned with the created task.
- Invalid date formats are rejected with an appropriate error message.	

Due date is optional. The date picker should prevent selecting previous dates, and backend validation should enforce the same rule.

US-2	As a team member, I want to update a task's due date so that I can adjust deadlines as work changes.	1. An existing due date can be changed to today or any future date.
- Attempting to update a task with a past due date is rejected with a validation error.
- Updating the due date does not modify unrelated task fields.
- Removing an existing due date is supported if the field remains optional.	

Frontend should restrict date selection to today and future dates, while backend validation prevents invalid updates.


US-3	As a team member, I want to identify overdue tasks so that I can prioritise work that has missed its deadline.	1. A task is considered overdue when its due date is before the current date and its status is not Done.
- Overdue tasks display a clear visual indicator in the task list.
- Tasks with future or no due dates are not marked as overdue.	

Overdue status should be computed consistently by the backend or frontend.

US-4	As a team member, I want to filter tasks by overdue status so that I can quickly find tasks requiring immediate attention.	1. Applying the overdue filter returns only tasks whose due date has passed and are not completed.
- Tasks without overdue status are excluded from the results.
- If no overdue tasks exist, the system returns an empty list without errors.	

Assumes an optional overdue query filter is supported.

FEATURE: TAGS

US-5	As a team member, I want to add tags to a task so that I can categorise related work.	1. A task can be created with zero or more tags.
- Tags are automatically trimmed before being stored.
- Empty, whitespace-only, or invalid tags are rejected with a validation error.
- Tags are returned when retrieving the task.	

Tags should have optional validation rules such as maximum number of tags and maximum tag length.

US-6	As a team member, I want to update task tags with suggestions from existing tags so that I can reuse consistent labels and avoid duplicates.	1. When typing a tag, the system suggests matching existing tags from other tasks.
- A user can select a suggested tag instead of creating a new similar tag.
- Empty or invalid tags are rejected during updates.
- Updating tags does not modify unrelated task fields.	

Tag suggestions are based on existing task data. The goal is to reduce duplicates such as "backend", "Backend", and "back-end".

US-7	As a team member, I want to filter tasks by tag so that I can quickly find related work items.	1. Filtering by a selected tag returns only tasks containing that exact tag.
- If no tasks match the selected tag, an empty result is returned.
- Tags remain preserved after unrelated task updates such as changing status or priority.	Filtering should use existing stored tags rather than partial text matching unless explicitly required later.

MY INPUT:

For US-1 and US-2, whenever creating or updating the date, do not allow the user to assign passed dates. You can start picking from the current day and forward. 

For US6 the app should suggest existing tasks once the user starts typing in order to avoid very close but different tags for the same concept.