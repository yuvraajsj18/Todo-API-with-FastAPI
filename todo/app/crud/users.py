from app import models, schemas
from app.security import get_password_hash
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(models.users.User).filter(models.users.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.users.User)
        .filter(models.users.User.username == username)
        .first()
    )


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.users.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.users.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.users.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
