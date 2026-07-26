from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_root_serves_frontend_html():
    response = client.get("/")
    assert response.status_code == 200
    assert "Task Tracker" in response.text


def test_task_creation_and_listing_work():
    response = client.post(
        "/tasks",
        json={"title": "Write integration test", "description": "Verify board flow"},
    )
    assert response.status_code == 201

    list_response = client.get("/tasks")
    assert list_response.status_code == 200
    tasks = list_response.json()
    assert any(task["title"] == "Write integration test" for task in tasks)


def test_task_update_priority_and_status():
    response = client.post(
        "/tasks",
        json={
            "title": "Fix bug",
            "description": "Update task fields",
            "status": "ToDo",
            "priority": "Low",
        },
    )
    assert response.status_code == 201
    task = response.json()

    update_response = client.patch(
        f"/tasks/{task['id']}",
        json={"priority": "High", "status": "InProgress"},
    )
    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["priority"] == "High"
    assert updated_task["status"] == "InProgress"

    same_status_response = client.patch(
        f"/tasks/{task['id']}",
        json={"priority": "Medium", "status": "InProgress"},
    )
    assert same_status_response.status_code == 200
    same_status_task = same_status_response.json()
    assert same_status_task["priority"] == "Medium"
    assert same_status_task["status"] == "InProgress"
