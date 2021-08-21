from typing import Dict
from app import schemas
from fastapi.testclient import TestClient
from app.tests import utils


def test_create_todo(client: TestClient, user_token_headers: Dict[str, str]):
    todo_in = schemas.TodoCreate(
        title=utils.random_lower_string(), description=utils.random_lower_string()
    )
    response = client.post("/todos/", json=todo_in.dict(), headers=user_token_headers)

    assert 200 <= response.status_code < 300

    todo = response.json()
    assert todo["title"] == todo_in.title


def test_read_all_todos(client: TestClient, user_token_headers: Dict[str, str]):
    todo1 = schemas.TodoCreate(
        title=utils.random_lower_string(), description=utils.random_lower_string()
    )
    response = client.post("/todos/", json=todo1.dict(), headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todo2 = schemas.TodoCreate(
        title=utils.random_lower_string(), description=utils.random_lower_string()
    )
    response = client.post("/todos/", json=todo2.dict(), headers=user_token_headers)
    assert 200 <= response.status_code < 300

    response = client.get("/todos/", headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todos = response.json()
    assert len(todos) > 0
    assert todos[-1]["title"] == todo2.title


def test_update_todo_complete(client: TestClient, user_token_headers: Dict[str, str]):
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    response = client.post("/todos/", json=todo_in.dict(), headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todo = response.json()
    assert todo["title"] == todo_in.title

    response = client.put(
        f"/todos/?todo_id={todo['id']}&complete=true", headers=user_token_headers
    )
    assert 200 <= response.status_code < 300

    todo = response.json()
    assert todo["title"] == todo_in.title
    assert todo["done"] is True


def test_update_todo_complete_when_not_found(
    client: TestClient, user_token_headers: Dict[str, str]
):
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    response = client.post("/todos/", json=todo_in.dict(), headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todo = response.json()
    assert todo["title"] == todo_in.title

    response = client.put(
        f"/todos/?todo_id={todo['id'] + 1}&complete=true", headers=user_token_headers
    )
    assert response.status_code == 404


def test_delete_todo(client: TestClient, user_token_headers: Dict[str, str]):
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    response = client.post("/todos/", json=todo_in.dict(), headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todo = response.json()
    assert todo["title"] == todo_in.title

    response = client.delete(f"/todos/{todo['id']}", headers=user_token_headers)
    assert 200 <= response.status_code < 300

    response = client.get("/todos/", headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todos = response.json()
    assert todo not in todos


def test_delete_todo_not_found(client: TestClient, user_token_headers: Dict[str, str]):
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    response = client.post("/todos/", json=todo_in.dict(), headers=user_token_headers)
    assert 200 <= response.status_code < 300

    todo = response.json()
    assert todo["title"] == todo_in.title

    response = client.delete(f"/todos/{todo['id'] + 1}", headers=user_token_headers)
    assert response.status_code == 404
