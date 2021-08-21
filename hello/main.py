from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


@app.get("/")
async def hello():
    return {"message": "Hello, World!"}


items = [
    {
        "item_id": 0,
        "name": "Item 1",
        "description": "Description for item 1",
        "price": 50.25,
    },
    {
        "item_id": 1,
        "name": "Item 2",
        "description": "Description for item 2",
        "price": 20.00,
        "tax": 2.0,
    },
    {
        "item_id": 2,
        "name": "Item 3",
        "description": "Description for item 3",
        "price": 30.00,
        "tax": 1.5,
    },
]

users = [
    {
        "id": 0,
        "username": "user1",
        "hashed_password": "somecrypticpassword1",
    },
    {
        "id": 1,
        "username": "user2",
        "hashed_password": "somecrypticpassword2",
    },
    {
        "id": 2,
        "username": "user2",
        "hashed_password": "somecrypticpassword2",
    },
]


@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., ge=0)):
    if item_id < len(items):
        return items[item_id]

    return {"Error": f"item_id {item_id} not found."}


async def common_parameters(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}


class CommonQueryParams:
    def __init__(self, skip: int = 0, limit: int = 10):
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return items[commons.skip : commons.skip + commons.limit]


@app.get("/users/")
async def read_users(commons: CommonQueryParams = Depends(CommonQueryParams)):
    return items[commons.skip : commons.skip + commons.limit]


@app.get("/greet")
async def greet(
    name: Optional[str] = Query(None, min_length=1, title="Name", alias="username")
):
    if name:
        return {"message": f"Hello, {name}"}
    return {"message": "Hello, Anonymous!"}


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(None, max_length=300)
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    items.append({"item_id": len(items), **item.dict()})
    return items[-1]


@app.put("/items/{item_id}")
async def update_item(item_id: int, add_price: float = Body(...)):
    if item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    item = Item(**items[item_id])
    item.price += add_price

    items[item_id] = item.dict()

    return items[item_id]
