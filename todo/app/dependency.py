from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, oauth2
from sqlalchemy.orm import Session

from app import crud
from app.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(db: Session, token: str = Depends(oauth2_scheme)):
    username = decode_access_token(token)
    user = crud.user.get_user_by_username(db, username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user
