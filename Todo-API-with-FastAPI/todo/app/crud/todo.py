from app import models, schemas
from sqlalchemy.orm import Session


def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.dict(), owner_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return (
        db.query(models.Todo)
        .filter(models.Todo.owner_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_todo_complete(db: Session, todo_id: int, complete: bool, user_id: int):
    db_todo = db.query(models.Todo).get(todo_id)
    if not db_todo:
        return None
    if db_todo.owner_id != user_id:
        raise Exception("Not authorized")
    db_todo.done = complete
    db.commit()
    db.refresh(db_todo)
    return db_todo


def delete_todo(
    db: Session,
    todo_id: int,
    user_id: int,
):
    db_todo = db.query(models.Todo).get(todo_id)

    if not db_todo:
        raise KeyError("Todo Not found")

    if db_todo.owner_id != user_id:
        raise Exception("Not authorized")

    db.delete(db_todo)
    db.commit()
