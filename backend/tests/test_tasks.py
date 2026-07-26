from datetime import date, timedelta


def test_create_task_valid_returns_201_with_full_body(client):
    payload = {
        "title": "New task",
        "description": "A description",
        "status": "ToDo",
        "priority": "High",
        "assignee": "alice",
        "due_date": date.today().isoformat(),
        "tags": ["urgent", "backend"],
    }

    response = client.post("/tasks", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["title"] == payload["title"]
    assert body["description"] == payload["description"]
    assert body["status"] == payload["status"]
    assert body["priority"] == payload["priority"]
    assert body["assignee"] == payload["assignee"]
    assert body["due_date"] == payload["due_date"]
    assert body["tags"] == payload["tags"]
    assert body["overdue"] is False
    assert body["id"]
    assert body["created_at"]
    assert body["updated_at"]


def test_create_task_missing_title_returns_422(client):
    payload = {"description": "Missing title"}

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_blank_title_returns_422(client):
    payload = {"title": "   "}

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_invalid_priority_returns_422(client):
    payload = {"title": "Task", "priority": "Urgent"}

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_create_task_unknown_field_returns_422(client):
    payload = {"title": "Task", "unknown": "value"}

    response = client.post("/tasks", json=payload)

    assert response.status_code == 422


def test_list_tasks_empty_returns_200_and_empty_list(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_status_no_match_returns_200_and_empty_list(client):
    client.post("/tasks", json={"title": "Task 1", "status": "Done"})
    response = client.get("/tasks", params={"status": "ToDo"})

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_filter_by_priority_returns_only_matches(client):
    client.post("/tasks", json={"title": "Low task", "priority": "Low"})
    client.post("/tasks", json={"title": "High task", "priority": "High"})

    response = client.get("/tasks", params={"priority": "High"})

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "High task"
    assert tasks[0]["priority"] == "High"


def test_get_task_by_id_returns_task(client, created_task):
    task_id = created_task["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_get_task_by_id_not_found_returns_404_with_detail(client):
    response = client.get("/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_patch_partial_update_keeps_other_fields(client, created_task):
    task_id = created_task["id"]
    payload = {"description": "Updated description"}

    response = client.patch(f"/tasks/{task_id}", json=payload)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == task_id
    assert body["description"] == payload["description"]
    assert body["title"] == created_task["title"]
    assert body["status"] == created_task["status"]
    assert body["priority"] == created_task["priority"]


def test_patch_not_found_returns_404(client):
    response = client.patch("/tasks/00000000-0000-0000-0000-000000000000", json={"description": "No task"})

    assert response.status_code == 404


def test_patch_valid_transition_todo_to_inprogress_returns_200(client, created_task):
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "InProgress"})

    assert response.status_code == 200
    assert response.json()["status"] == "InProgress"


def test_patch_invalid_transition_todo_to_done_returns_422(client, created_task):
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "Done"})

    assert response.status_code == 422


def test_patch_due_date_in_past_returns_422(client, created_task):
    task_id = created_task["id"]
    past_due_date = (date.today() - timedelta(days=1)).isoformat()

    response = client.patch(f"/tasks/{task_id}", json={"due_date": past_due_date})

    assert response.status_code == 422
    assert "due date" in response.json()["detail"][0]["msg"].lower()


def test_patch_same_status_returns_422(client, created_task):
    task_id = created_task["id"]

    response = client.patch(f"/tasks/{task_id}", json={"status": "ToDo"})

    assert response.status_code == 422


def test_delete_existing_returns_204_no_body(client, created_task):
    task_id = created_task["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""


def test_delete_missing_returns_404(client):
    response = client.delete("/tasks/00000000-0000-0000-0000-000000000000")

    assert response.status_code == 404
