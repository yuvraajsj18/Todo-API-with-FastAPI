import random
import string
from typing import Dict
from app import crud, models, schemas

from sqlalchemy.orm import Session
from fastapi.testclient import TestClient


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 32)))


def create_random_user(db: Session) -> models.User:
    username = random_lower_string()
    password = random_lower_string()
    user_in = schemas.UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    return user


def user_authentication_headers(
    *, client: TestClient, username: str, password: str
) -> Dict[str, str]:
    data = {"username": username, "password": password}
    r = client.post("/token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token(*, client: TestClient, db: Session) -> Dict[str, str]:
    """
    Return a valid token for a random user
    """
    username = random_lower_string()
    password = random_lower_string()
    crud.create_user(db, user=schemas.UserCreate(username=username, password=password))
    return user_authentication_headers(
        client=client, username=username, password=password
    )
