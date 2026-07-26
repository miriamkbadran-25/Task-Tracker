from datetime import date, datetime, timedelta

from fastapi.testclient import TestClient

from app import storage
from app.main import app
from app.models import TaskPriority, TaskResponse, TaskStatus


client = TestClient(app)


def setup_function():
    storage._reset()


def test_create_task_with_future_due_date():
    response = client.post(
        "/tasks",
        json={"title": "Ship feature", "due_date": str(date.today() + timedelta(days=1))},
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["due_date"] == str(date.today() + timedelta(days=1))
    assert payload["overdue"] is False


def test_past_due_date_is_rejected():
    response = client.post(
        "/tasks",
        json={"title": "Late task", "due_date": str(date.today() - timedelta(days=1))},
    )

    assert response.status_code == 422


def test_overdue_filter_returns_only_overdue_tasks():
    storage._tasks["overdue-id"] = TaskResponse(
        id="overdue-id",
        title="Overdue task",
        description="",
        status=TaskStatus.TODO,
        priority=TaskPriority.MEDIUM,
        assignee=None,
        due_date=date.today() - timedelta(days=1),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    client.post(
        "/tasks",
        json={"title": "Future task", "due_date": str(date.today() + timedelta(days=1))},
    )
    storage._tasks["done-id"] = TaskResponse(
        id="done-id",
        title="Done task",
        description="",
        status=TaskStatus.DONE,
        priority=TaskPriority.MEDIUM,
        assignee=None,
        due_date=date.today() - timedelta(days=1),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    overdue_response = client.get("/tasks", params={"overdue": True})
    assert overdue_response.status_code == 200
    overdue_titles = [task["title"] for task in overdue_response.json()]
    assert overdue_titles == ["Overdue task"]

    non_overdue_response = client.get("/tasks", params={"overdue": False})
    assert non_overdue_response.status_code == 200
    non_overdue_titles = [task["title"] for task in non_overdue_response.json()]
    assert set(non_overdue_titles) == {"Future task", "Done task"}
