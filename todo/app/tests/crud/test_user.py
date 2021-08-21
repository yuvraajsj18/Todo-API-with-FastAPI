from app import crud
from app.schemas import UserCreate
from app.tests import utils
from sqlalchemy.orm import Session


def test_create_user(db: Session):
    """Test creating a user."""
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    assert user.username == username
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session):
    """Test authenticating a user."""
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    authenticated_user = crud.users.authenticate_user(
        db, username=username, password=password
    )
    assert authenticated_user
    assert authenticated_user.username == user.username


def test_not_authenticate_user(db: Session):
    """Test not authenticating a user."""
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    assert not crud.authenticate_user(db, username=username, password="wrong")
    assert not crud.authenticate_user(db, username="wrong", password=password)
    assert not crud.authenticate_user(db, username="wrong", password="wrong")


def test_get_user_by_id(db: Session):
    """Test getting a user by id."""
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    user_out = crud.get_user(db, user_id=user.id)
    assert user_out
    assert user_out.username == user.username
    assert user_out.hashed_password == user.hashed_password


def test_get_user_by_username(db: Session):
    """Test getting a user by username."""
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    user_out = crud.get_user_by_username(db, username=username)
    assert user_out
    assert user_out.username == user.username
    assert user_out.hashed_password == user.hashed_password


def test_get_users(db: Session):
    """Test getting all users."""
    username = utils.random_lower_string()
    password = utils.random_lower_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.create_user(db, user=user_in)
    user_out = crud.get_users(db)
    print(user_out)
    assert user_out
    assert user_out[-1].username == user.username
    assert user_out[-1].hashed_password == user.hashed_password
