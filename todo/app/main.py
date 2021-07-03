from fastapi import FastAPI

from app.routers import users

app = FastAPI()


@app.get("/")
async def root():
    return {"app": "Todo API"}
