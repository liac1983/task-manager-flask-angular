# backend/tests/test_tasks.py

def register_and_login(client):
    """Helper to create a user and obtain a JWT token."""
    client.post(
        "/register",
        json={
            "username": "lara",
            "email": "lara@example.com",
            "password": "123456",
        },
    )

    response = client.post(
        "/login",
        json={"username": "lara", "password": "123456"},
    )
    data = response.get_json()
    return data["access_token"]


def test_tasks_requires_auth(client):
    """The /tasks route should reject requests without a JWT token."""
    response = client.get("/tasks")
    assert response.status_code == 401  # Unauthorized
    data = response.get_json()
    assert "authorization" in data["msg"].lower()


def test_create_and_list_tasks_with_token(client):
    """Should allow creating and listing tasks when authenticated."""
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Initially, list should be empty
    response_list_empty = client.get("/tasks", headers=headers)
    assert response_list_empty.status_code == 200
    assert response_list_empty.get_json() == []

    # Create a new task
    response_create = client.post(
        "/tasks",
        headers=headers,
        json={"title": "Test task", "description": "From pytest"},
    )
    assert response_create.status_code == 201

    # List again
    response_list = client.get("/tasks", headers=headers)
    assert response_list.status_code == 200
    tasks = response_list.get_json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test task"
    assert tasks[0]["description"] == "From pytest"
    assert tasks[0]["done"] is False


def test_task_has_created_at_and_default_category(client):
    """New tasks should have a created_at date and a default category."""
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    response_create = client.post(
        "/tasks",
        headers=headers,
        json={"title": "With date", "description": "Check created_at"},
    )
    assert response_create.status_code == 201

    response_list = client.get("/tasks", headers=headers)
    assert response_list.status_code == 200
    tasks = response_list.get_json()
    assert len(tasks) == 1

    task = tasks[0]
    assert task["category"] == "personal"  # default from model
    assert task["created_at"] is not None


def test_invalid_category_falls_back_to_other(client):
    """If an invalid category is sent, it should become 'other'."""
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    response_create = client.post(
        "/tasks",
        headers=headers,
        json={"title": "Invalid cat", "description": "", "category": "banana"},
    )
    assert response_create.status_code == 201

    response_list = client.get("/tasks", headers=headers)
    tasks = response_list.get_json()
    assert len(tasks) == 1
    assert tasks[0]["category"] == "other"


def test_completed_at_set_when_task_marked_done(client):
    """completed_at should be set when task is marked as done."""
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create task
    response_create = client.post(
        "/tasks",
        headers=headers,
        json={"title": "Complete me", "description": "Test completed_at"},
    )
    assert response_create.status_code == 201
    task_id = response_create.get_json()["id"]

    # Mark as done
    response_update = client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={"done": True},
    )
    assert response_update.status_code == 200

    # Fetch task
    response_list = client.get("/tasks", headers=headers)
    tasks = response_list.get_json()
    assert len(tasks) == 1
    task = tasks[0]

    assert task["done"] is True
    assert task["completed_at"] is not None


def test_completed_at_cleared_when_task_marked_undone(client):
    """completed_at should be cleared if task is marked back as not done."""
    token = register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create and mark as done
    response_create = client.post(
        "/tasks",
        headers=headers,
        json={"title": "Toggle done", "description": ""},
    )
    task_id = response_create.get_json()["id"]

    client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={"done": True},
    )

    # Now mark as not done
    response_update = client.put(
        f"/tasks/{task_id}",
        headers=headers,
        json={"done": False},
    )
    assert response_update.status_code == 200

    # Fetch task
    response_list = client.get("/tasks", headers=headers)
    task = response_list.get_json()[0]

    assert task["done"] is False
    assert task["completed_at"] is None
