from app import schemas
from fastapi import APIRouter
from fastapi.param_functions import Depends
from app.dependency import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.users.User)
async def read_users_me(current_user: schemas.users.User = Depends(get_current_user)):
    return current_user
