import pytest
from app import crud, models, schemas
from app.tests import utils
from sqlalchemy.orm import Session


def test_create_todo(db: Session, user: models.User) -> None:
    """Test creating a todo"""
    todo_in = schemas.TodoCreate(
        title=utils.random_lower_string(),
        description=utils.random_lower_string(),
        done=False,
    )
    todo_out = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    assert todo_out.title == todo_in.title
    assert todo_out.owner_id == user.id


def test_get_todos(db: Session, user: models.User) -> None:
    """Test getting all todos"""
    todo_in_1 = schemas.TodoCreate(title=utils.random_lower_string())
    crud.create_todo(db=db, todo=todo_in_1, user_id=user.id)
    todo_in_2 = schemas.TodoCreate(title=utils.random_lower_string())
    crud.create_todo(db=db, todo=todo_in_2, user_id=user.id)
    todos = crud.get_todos(db=db, user_id=user.id)
    assert len(todos) == 2
    assert todos[0].title == todo_in_1.title
    assert todos[1].title == todo_in_2.title


def test_update_todo_complete(db: Session, user: models.User) -> None:
    """Test updating a todo's complete status"""
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    todo = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    todo_out = crud.update_todo_complete(
        db=db, todo_id=todo.id, complete=True, user_id=user.id
    )
    assert todo_out.done is True


def test_update_todo_complete_when_todo_does_not_exist(
    db: Session, user: models.User
) -> None:
    """Test updating a todo's complete status when todo doesn't exist"""
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    todo = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    todo_out = crud.update_todo_complete(
        db=db, todo_id=todo.id + 1, complete=True, user_id=user.id
    )
    assert todo_out is None


def test_update_todo_complete_when_todo_is_not_owned(
    db: Session, user: models.User
) -> None:
    """Test updating a todo's complete status when todo is not owned"""
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    todo = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    with pytest.raises(Exception) as e:
        todo_out = crud.update_todo_complete(
            db=db, todo_id=todo.id, complete=True, user_id=user.id + 1
        )


def test_delete_todo(db: Session, user: models.User) -> None:
    """Test deleting a todo"""
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    todo = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    crud.delete_todo(db=db, todo_id=todo.id, user_id=user.id)
    todos = crud.get_todos(db=db, user_id=user.id)
    assert todo not in todos


def test_delete_todo_when_todo_does_not_exist(db: Session, user: models.User) -> None:
    """Test deleting a todo when todo doesn't exist"""
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    todo = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    with pytest.raises(KeyError) as e:
        crud.delete_todo(db=db, todo_id=todo.id + 1, user_id=user.id)
    todos = crud.get_todos(db=db, user_id=user.id)
    assert todo in todos


def test_delete_todo_when_todo_is_not_owned(db: Session, user: models.User) -> None:
    """Test deleting a todo when todo is not owned"""
    todo_in = schemas.TodoCreate(title=utils.random_lower_string())
    todo = crud.create_todo(db=db, todo=todo_in, user_id=user.id)
    with pytest.raises(Exception) as e:
        crud.delete_todo(db=db, todo_id=todo.id, user_id=user.id + 1)
    todos = crud.get_todos(db=db, user_id=user.id)
    assert todo in todos
