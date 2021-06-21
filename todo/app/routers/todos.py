from fastapi import APIRouter

router = APIRouter(prefix="/todos", tags=["todos"])


@router.get("/")
async def read_todos():
    return "To Be Implemented"
