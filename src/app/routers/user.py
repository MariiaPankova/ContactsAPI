from contextlib import asynccontextmanager
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from src import models
from src.infrastructure.database import create_db_and_tables, get_session

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=models.user.UserRead)
def create_user(user: models.user.UserCreate, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.get("/", response_model=List[models.user.UserRead])
def read_users(session: Session = Depends(get_session)):
    q = select(models.user.User)
    users = session.exec(q).all()
    return users


@router.get("/{user_email}", response_model=models.user.UserRead)
def get_user(user_email: str, session: Session = Depends(get_session)):
    q = select(models.user.User).where(models.user.User.email == user_email)
    user = session.exec(q).first()
    if user is None:
        raise HTTPException(404, "User not found")
    return user


@router.patch("/{user_id}", response_model=models.user.UserRead)
def update_user(
    user_id: int, user: models.user.UserUpdate, session: Session = Depends(get_session)
):
    db_user = session.get(models.user.User, user_id)
    if db_user is None:
        raise HTTPException(404, "User not found")
    user_dict = user.dict(exclude_unset=True)
    for k, v in user_dict.items():
        setattr(db_user, k, v)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(models.user.User, user_id)
    if db_user is None:
        raise HTTPException(404, "User not found")
    session.delete(db_user)
    session.commit()
    return {"ok": True}


@router.get(
    "/{user_id}/folders", response_model=List[models.folder.FolderRead], tags=["folder"]
)
def get_user_folders(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(models.user.User, user_id)
    if db_user is None:
        raise HTTPException(404, "User not found")
    return db_user.folders
