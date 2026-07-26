from fastapi.testclient import TestClient

from app.main import app
from app import storage


client = TestClient(app)


def setup_function():
    storage._reset()


def test_create_task_with_tags_and_return_tags():
    response = client.post(
        "/tasks",
        json={"title": "Ship feature", "tags": [" backend ", "API", "frontend "]},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["tags"] == ["Backend", "API", "Frontend"]


def test_update_task_tags_preserves_unrelated_fields():
    create_response = client.post(
        "/tasks",
        json={
            "title": "Fix bug",
            "description": "Needs review",
            "status": "ToDo",
            "priority": "Low",
            "assignee": "Alice",
            "tags": ["backend"],
        },
    )
    task_id = create_response.json()["id"]

    update_response = client.patch(
        f"/tasks/{task_id}",
        json={"tags": [" api ", "frontend"]},
    )

    assert update_response.status_code == 200
    payload = update_response.json()
    assert payload["tags"] == ["Api", "Frontend"]
    assert payload["title"] == "Fix bug"
    assert payload["description"] == "Needs review"
    assert payload["status"] == "ToDo"
    assert payload["priority"] == "Low"
    assert payload["assignee"] == "Alice"


def test_filter_tasks_by_exact_tag_is_case_insensitive():
    client.post("/tasks", json={"title": "One", "tags": ["backend"]})
    client.post("/tasks", json={"title": "Two", "tags": ["frontend"]})
    client.post("/tasks", json={"title": "Three", "tags": ["backend", "api"]})

    response = client.get("/tasks", params={"tag": "Backend"})

    assert response.status_code == 200
    assert [task["title"] for task in response.json()] == ["One", "Three"]


def test_create_task_normalizes_tags_to_camel_case():
    response = client.post(
        "/tasks",
        json={"title": "Ship feature", "tags": [" backend ", "my-tag", "API", "frontend "]},
    )

    assert response.status_code == 201
    assert response.json()["tags"] == ["Backend", "MyTag", "API", "Frontend"]


def test_tag_suggestions_return_existing_tags():
    client.post("/tasks", json={"title": "One", "tags": ["backend"]})
    client.post("/tasks", json={"title": "Two", "tags": ["frontend"]})
    client.post("/tasks", json={"title": "Three", "tags": ["API"]})

    response = client.get("/tags/suggestions", params={"q": "back"})

    assert response.status_code == 200
    assert response.json() == ["Backend"]


def test_empty_tag_query_returns_all_existing_tags():
    client.post("/tasks", json={"title": "One", "tags": ["backend"]})
    client.post("/tasks", json={"title": "Two", "tags": ["frontend"]})

    response = client.get("/tags/suggestions", params={"q": ""})

    assert response.status_code == 200
    assert response.json() == ["Backend", "Frontend"]
