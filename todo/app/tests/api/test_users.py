from typing import Dict

from app import models, schemas
from fastapi.testclient import TestClient
from app.tests import utils


def test_create_user(client: TestClient):
    user = schemas.UserCreate(username="test", password="test")
    response = client.post("/users/", json=user.dict())
    assert 200 <= response.status_code < 300
    created_user = response.json()
    assert created_user["username"] == user.username


def test_create_user_when_exist(client: TestClient):
    user = schemas.UserCreate(username="existing", password="existing")
    response = client.post("/users/", json=user.dict())
    assert 200 <= response.status_code < 300
    response = client.post("/users/", json=user.dict())
    assert 400 <= response.status_code < 500


def test_read_users(client: TestClient, user_token_headers: Dict[str, str]):
    user1 = schemas.UserCreate(
        username=utils.random_lower_string(), password=utils.random_lower_string()
    )
    response = client.post("/users/", json=user1.dict())
    assert 200 <= response.status_code < 300

    user2 = schemas.UserCreate(
        username=utils.random_lower_string(), password=utils.random_lower_string()
    )
    response = client.post("/users/", json=user2.dict())
    assert 200 <= response.status_code < 300

    response = client.get("/users/", headers=user_token_headers)
    assert 200 <= response.status_code < 300
    users = response.json()
    assert len(users) > 0
    assert users[-1]["username"] == user2.username


def test_read_user_me(client: TestClient, user_token_headers: Dict[str, str]):
    response = client.get("/users/me", headers=user_token_headers)
    assert 200 <= response.status_code < 300
    current_user = response.json()
    assert current_user
    assert "username" in current_user


def test_read_user(
    client: TestClient, user_token_headers: Dict[str, str], user: models.User
):
    user_id = user.id
    response = client.get(f"/users/{user_id}", headers=user_token_headers)
    assert 200 <= response.status_code < 300
    existing_user = response.json()
    assert existing_user
    assert existing_user["username"] == user.username


def test_read_user_when_not_found(
    client: TestClient, user_token_headers: Dict[str, str], user: models.User
):
    response = client.get(f"/users/{user.id + 1}", headers=user_token_headers)
    assert response.status_code == 404
