from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from app import crud, schemas
from app.dependency import get_db, get_current_user
from sqlalchemy.orm import Session

router = APIRouter(prefix="/todos", tags=["todos"])


@router.post("/", response_model=schemas.Todo)
async def create_todo(
    todo: schemas.TodoCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    todo = crud.create_todo(
        db,
        todo,
        current_user.id,
    )
    return todo


@router.get("/", response_model=List[schemas.Todo])
async def read_all_todos(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    todos = crud.get_todos(db, current_user.id, skip, limit)
    return todos


@router.put("/", response_model=schemas.Todo)
async def update_todo_complete(
    todo_id: int,
    complete: bool,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    try:
        todo = crud.update_todo_complete(
            db,
            todo_id,
            complete,
            current_user.id,
        )
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )
    return todo


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    try:
        crud.delete_todo(db, todo_id, current_user.id)
    except KeyError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    return "Todo Deleted"
