<FEATURE: DUE DATE>

## Prompt 1 — Add Task Tags to Data Models
You are a senior Python backend engineer. Add backend model support for task tags to my existing FastAPI app.

Context files:
@app/models.py

The application already supports creating, retrieving, updating, filtering, and deleting tasks. The frontend create and edit buttons already exist, so only implement the backend changes required for tags.

Goal:
Update the data models to support task tags.

Requirements:

- Add a tags field to the relevant Task request/response models.
- Tags should be:
  - A list of strings.
  - Default to an empty list when not provided.

Add validation rules:
- Trim leading and trailing whitespace from every tag before storing.
- Reject empty strings or whitespace-only tags.
- Reject invalid tags.
- Support optional validation limits:
  - Maximum number of tags per task.
  - Maximum tag length.

Implementation rules:
- Keep Pydantic responsible for request validation.
- Follow the existing project style and naming conventions.
- Do not modify unrelated models.
- Do not add new dependencies.

Modify only:
@app/models.py


## Prompt 2 — Add Storage Support for Task Tags
You are a senior Python backend engineer. Add storage support for task tags to my existing FastAPI app.

Context files:
@app/storage.py

The application already supports creating, retrieving, updating, filtering, and deleting tasks.

Goal:
Extend the existing in-memory storage behavior to support task tags.

Requirements:

- Existing task creation must store tags.
- Existing task retrieval must return tags.
- Existing task updates must preserve tags unless tags are explicitly updated.
- Updating tags must not modify:
  - title
  - description
  - status
  - priority
  - assignee
  - other unrelated fields

Implementation constraints:
- Do not redesign the storage architecture.
- Do not introduce a database.
- Do not add new dependencies.
- Do not add try/except blocks around storage operations.
- Follow the existing project style and naming conventions.

Modify only:
@app/storage.py


## Prompt 3 — Add Tag Suggestion API Endpoint
You are a senior Python backend engineer. Add tag suggestion support to my existing FastAPI app.

Context files:
@app/main.py
@app/models.py
@app/storage.py

The application already supports creating, retrieving, updating, filtering, and deleting tasks.
Task tags are already supported in the backend.

Goal:
Create an endpoint that suggests existing tags based on stored task data.

Add ONE new route:

Route:
GET /tags/suggestions

Exact specification:

Query parameter:
- q: str

Response model:
- list[str]

Behavior:
- Search existing stored tasks and collect existing tags.
- Return matching tags based on the typed text.
- Suggestions should help avoid duplicate concepts.
- Matching should be case-insensitive.
- Prefer returning existing stored versions of tags.

Example:

Existing tags:
["backend", "frontend", "API"]

Query:
"back"

Response:
["backend"]

Rules:
- Do not create new tags from the query.
- Do not use external search libraries.
- Do not use fuzzy matching libraries.
- Do not modify unrelated routes.
- Follow the existing project style and naming conventions.

Modify only:
@app/main.py


## Prompt 4 — Add Task Filtering by Tag
You are a senior Python backend engineer. Extend task filtering to support filtering by tags in my existing FastAPI app.

Context files:
@app/main.py
@app/models.py
@app/storage.py

The application already supports filtering tasks by status and priority.

Goal:
Extend the existing GET /tasks route to support tag filtering.

Requirements:

Existing GET /tasks route should support:

Optional query parameter:
- tag: str | None = None

Behavior:
- If tag is provided:
  - Return only tasks containing that exact tag.
  - Matching should use stored tags.
  - Do not use partial matching.
  - Do not treat "Backend" and "backend" as different tags after validation/normalization.

- If no tasks match:
  - Return status code: 200
  - Response: []

Existing status and priority filters must continue working.

Implementation constraints:
- Do not modify unrelated routes.
- Do not redesign the architecture.
- Do not introduce a database.
- Do not add authentication.
- Do not add new dependencies.
- Do not add try/except blocks around storage operations.
- Do not manually validate query enum values.
- Do not return 404 for empty results.
- Do not change existing task behavior except where required to support tags.

Follow the existing project style and naming conventions.

Modify only:
@app/main.py
@app/storage.py if required

<FEATURE: TAG>

## Prompt 1 — Add Due Date Support When Creating Tasks (US-1)
You are a senior Python backend engineer. Add due date support when creating tasks to my existing FastAPI app.

Context files:
@app/main.py
@app/models.py
@app/storage.py

Existing application context:
- The app is a Task Tracker built with FastAPI.
- Tasks already support title, description, status, priority, and assignee.
- Task creation and update routes already exist.
- Do not redesign the architecture.
- Keep the existing layered structure:
  - models.py → Pydantic request/response models and validation rules
  - storage.py → in-memory task storage operations
  - main.py → API routes only

Generate ONLY the backend changes required to support due date creation.

Required feature scope:

Add optional due date support when creating tasks (US-1)

Requirements:
- Tasks can have an optional due_date field.
- due_date must be stored and returned in task responses.
- due_date must accept today or any future date.
- Past dates must be rejected with a validation error.
- Invalid date formats must be rejected by Pydantic/FastAPI validation.
- Keep due_date optional (None is valid).

Backend validation:
- Validation must exist in the Pydantic model layer.
- Do not rely only on frontend date picker restrictions.
- Use the current system date when validating.
- Do not hard-code dates.

Files to modify:

@app/models.py
Required changes:
- Add due_date field to task request/response models.
- Add validation ensuring due_date is today or later.
- Keep existing Pydantic v2 style.

@app/storage.py
Required changes:
- Update task creation to store due_date.
- Preserve backward compatibility with tasks created before due_date existed.
- Do not introduce external databases or dependencies.

@app/main.py
Required changes:
- Update existing POST /tasks route only as needed for due_date.
- Keep existing route behavior unchanged.

Imports to add only if missing:
from datetime import date

DO NOT:
- DO NOT create a new endpoint.
- DO NOT modify unrelated routes.
- DO NOT change existing task fields or behavior.
- DO NOT manually parse dates from strings.
- DO NOT manually validate enum values; Pydantic/FastAPI handles invalid enum values.
- DO NOT add try/except blocks around validation or storage calls.
- DO NOT introduce authentication, database models, or migrations.
- DO NOT add frontend code.
- DO NOT refactor existing architecture.

Implementation expectations:
- Follow the existing coding style in the project.
- Verify that existing tests and routes continue working.

Output only:
1. Imports that need to be added.
2. Modified/new Python code sections only.
3. Put everything in a single code block.


## Prompt 2 — Add Due Date Support When Updating Tasks (US-2)
You are a senior Python backend engineer. Add due date update support to my existing FastAPI app.

Context files:
@app/main.py
@app/models.py
@app/storage.py

Existing application context:
- The app is a Task Tracker built with FastAPI.
- Tasks already support title, description, status, priority, and assignee.
- Task creation and update routes already exist.
- Do not redesign the architecture.
- Keep the existing layered structure:
  - models.py → Pydantic request/response models and validation rules
  - storage.py → in-memory task storage operations
  - main.py → API routes only

Generate ONLY the backend changes required to support updating due dates.

Required feature scope:

Add due date support when updating tasks (US-2)

Requirements:
- Existing tasks can have their due_date updated.
- New due_date values must follow the same validation rules:
  - today or future date is valid.
  - past dates are rejected.
- Removing an existing due_date must be supported by allowing None.
- Updating due_date must not overwrite unrelated fields.
- Preserve all existing update behavior and status transition rules.

Backend validation:
- Validation must exist in the Pydantic model layer.
- Use the current system date when validating.
- Do not hard-code dates.

Files to modify:

@app/models.py
Required changes:
- Add due_date field to update request models if needed.
- Add validation ensuring due_date is today or later.
- Keep existing Pydantic v2 style.

@app/storage.py
Required changes:
- Update task update logic to support changing/removing due_date.
- Ensure unrelated fields are preserved.
- Do not introduce external databases or dependencies.

@app/main.py
Required changes:
- Update existing PATCH/PUT task update route only as needed for due_date.
- Keep existing route behavior unchanged.

Imports to add only if missing:
from datetime import date

DO NOT:
- DO NOT create a new endpoint.
- DO NOT modify unrelated routes.
- DO NOT change existing task fields or behavior.
- DO NOT manually parse dates from strings.
- DO NOT manually validate enum values; Pydantic/FastAPI handles invalid enum values.
- DO NOT add try/except blocks around validation or storage calls.
- DO NOT introduce authentication, database models, or migrations.
- DO NOT add frontend code.
- DO NOT refactor existing architecture.

Implementation expectations:
- Follow the existing coding style in the project.
- Verify that existing tests and routes continue working.

Output only:
1. Imports that need to be added.
2. Modified/new Python code sections only.
3. Put everything in a single code block.


## Prompt 3 — Add Overdue Detection and Filtering (US-3 + US-4)
You are a senior Python backend engineer. Add overdue task detection and filtering support to my existing FastAPI app.

Context files:
@app/main.py
@app/models.py
@app/storage.py

Existing application context:
- The app is a Task Tracker built with FastAPI.
- Tasks already support title, description, status, priority, assignee, and due_date.
- Task creation and update routes already exist.
- Do not redesign the architecture.
- Keep the existing layered structure:
  - models.py → Pydantic request/response models and validation rules
  - storage.py → in-memory task storage operations
  - main.py → API routes only

Generate ONLY the backend changes required to support overdue functionality.

Required feature scope:

1. Add overdue task detection (US-3)

Definition:
A task is overdue when:
- due_date exists
- due_date is before today's date
- task status is not Done

Implementation requirements:
- Overdue status must be computed dynamically.
- Do not store overdue as a database/storage field.
- Add overdue information to the response model if needed.
- Existing tasks with no due_date must never be overdue.
- Existing tasks with status Done must never be overdue.

---

2. Add overdue filtering support (US-4)

Requirements:
- Extend GET /tasks filtering to support overdue tasks.
- Add an optional query parameter:
  - overdue: bool | None = None

Behavior:
- overdue=true:
  - Return only tasks where:
    - due_date < today
    - status != Done
- overdue=false:
  - Return only tasks that are not overdue.
- overdue=None:
  - Keep existing behavior and return all tasks based on existing filters.
- Empty results return 200 with [].

Files to modify:

@app/models.py
Required changes:
- Add computed overdue field to TaskResponse if appropriate.
- Keep existing Pydantic v2 style.

@app/storage.py
Required changes:
- Extend task retrieval/filtering to support overdue filtering.
- Compute overdue dynamically based on current date and task status.
- Do not store overdue permanently.
- Do not introduce external databases or dependencies.

@app/main.py
Required changes:
- Update GET /tasks route to accept:
  - status: TaskStatus | None = None
  - priority: TaskPriority | None = None
  - overdue: bool | None = None
- Keep response model as:
  list[TaskResponse]

Imports to add only if missing:
from datetime import date
from app.models import TaskStatus, TaskPriority, TaskResponse
from app import storage

DO NOT:
- DO NOT create a new endpoint.
- DO NOT modify unrelated routes.
- DO NOT store overdue permanently.
- DO NOT manually parse dates from strings.
- DO NOT manually validate enum values; Pydantic/FastAPI handles invalid enum values.
- DO NOT add try/except blocks around validation or storage calls.
- DO NOT introduce authentication, database models, or migrations.
- DO NOT add frontend code.
- DO NOT refactor existing architecture.

Implementation expectations:
- Follow the existing coding style in the project.
- Preserve backward compatibility with tasks created before due_date existed.
- Verify that existing tests and routes continue working.

Output only:
1. Imports that need to be added.
2. Modified/new Python code sections only.
3. Put everything in a single code block.


I used ai to write these prompts. The context was, you are a prompt engineer. I gave it the inputs of the given prompt library to use as a skeleton.The only issue was that he wanted to place them all in the same prompt. Other than that he did a great job.