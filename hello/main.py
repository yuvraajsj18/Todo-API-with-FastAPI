from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

#################################################################
# I have added this here because I used codespaces to develop the app
# which make request from a different URL/origin, you won't find this in the
# article. To learn about CORS and how to set it up in FastAPI:
# https://fastapi.tiangolo.com/tutorial/cors/
# you can ignore this, if you are using localhost.

origins = [
    "https://yuvraajsj18-todo-api-with-fastapi-xcj4-8000.githubpreview.dev",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#################################################################


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


@app.get("/items/{item_id}")
async def get_item(item_id: int = Path(..., ge=0)):
    if item_id < len(items):
        return items[item_id]

    return {"Error": f"item_id {item_id} not found."}


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return items[skip : skip + limit]


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


@app.post("/items/")
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
