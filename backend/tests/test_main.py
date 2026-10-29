from fastapi.testclient import TestClient

from app import tasks
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "welcome"}


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_openapi_metadata():
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Task Manager API"
    assert response.json()["info"]["version"] == "0.1.0"

def test_get_tasks():
    response = client.get("/tasks")
    response1 = client.get("/tasks?completed=True")
    response2 = client.get("/tasks?completed=False")

    assert response.status_code == 200
    assert response1.status_code == 200
    assert response2.status_code == 200

    assert response.json() == [{"task_id":1,"description":"xyz","completed":True},{"task_id":2,"description":"abc","completed":False},{"task_id":3,"description":"pqr","completed":True},{"task_id":4,"description":"efg","completed":False}]
    assert response1.json() == [{"task_id":1,"description":"xyz","completed":True},{"task_id":3,"description":"pqr","completed":True}]
    assert response2.json() == [{"task_id":2,"description":"abc","completed":False},{"task_id":4,"description":"efg","completed":False}]

def test_get_task_by_id_valid():
    response_1 = client.get("/tasks/1")

    assert response_1.status_code == 200
    assert response_1.json() == {"task_id":1,"description":"xyz", "completed": True}

def test_get_task_by_id_invalid():
    response_999 = client.get("/tasks/999")

    assert response_999.status_code == 404
    assert response_999.json() == {"detail": "Task with id = 999 not found."}

def test_filter_incomplete_when_all_tasks_completed(monkeypatch):
    all_completed = [
        {"task_id": 1, "description": "Task A", "completed": True},
        {"task_id": 2, "description": "Task B", "completed": True},
    ]

    monkeypatch.setattr(tasks, "tasks", all_completed)

    response = client.get("/tasks?completed=false")

    assert response.status_code == 200
    assert response.json() == []


def test_filter_completed_when_all_tasks_incomplete(monkeypatch):
    all_incomplete = [
        {"task_id": 1, "description": "Task A", "completed": False},
        {"task_id": 2, "description": "Task B", "completed": False},
    ]

    monkeypatch.setattr(tasks, "tasks", all_incomplete)

    response = client.get("/tasks?completed=true")

    assert response.status_code == 200
    assert response.json() == []

def test_create_tasks(monkeypatch):

    dummy_tasks = [
        {"task_id": 1, "description": "Task A", "completed": False},
        {"task_id": 2, "description": "Task B", "completed": True},
    ]

    monkeypatch.setattr(tasks, "tasks", dummy_tasks)
    
    response = client.post("/tasks", json={"description": "this is a new task."})

    assert response.status_code == 201
    assert response.json()["task_id"] == 3
    assert response.json()["description"] == "this is a new task."
    assert response.json()["completed"] == False

    created_task_id = response.json()["task_id"]
    response_get = client.get(f"/tasks/{created_task_id}")

    assert response_get.json()["task_id"] == created_task_id
    assert response_get.json()["description"] == "this is a new task."
    assert response_get.json()["completed"] == False

def test_create_task_empty_description(monkeypatch):

    dummy_tasks = [
        {"task_id": 1, "description": "Task A", "completed": False},
        {"task_id": 2, "description": "Task B", "completed": True},
    ]

    monkeypatch.setattr(tasks, "tasks", dummy_tasks)
    
    response = client.post("/tasks", json={"description": ""})

    assert response.status_code == 422