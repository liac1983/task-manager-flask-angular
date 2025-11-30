# backend/tests/test_auth.py

def test_register_success(client):
  """Should register a new user successfully."""
  response = client.post(
      "/register",
      json={
          "username": "lara",
          "email": "lara@example.com",
          "password": "123456",
      },
  )

  assert response.status_code == 201
  data = response.get_json()
  assert data["msg"].lower().startswith("user registered")


def test_register_existing_user(client):
  """Should not allow registering an existing username/email."""
  payload = {
      "username": "lara",
      "email": "lara@example.com",
      "password": "123456",
  }

  # First registration
  response1 = client.post("/register", json=payload)
  assert response1.status_code == 201

  # Second registration with same data
  response2 = client.post("/register", json=payload)
  assert response2.status_code == 400
  data = response2.get_json()
  assert "already exists" in data["msg"].lower()


def test_login_success(client):
  """Should log in with valid credentials and return a JWT token."""

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

  assert response.status_code == 200
  data = response.get_json()
  assert "access_token" in data
  assert isinstance(data["access_token"], str)
