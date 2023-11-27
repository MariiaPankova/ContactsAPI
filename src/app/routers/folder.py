from contextlib import asynccontextmanager
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from src import models
from src.infrastructure.database import create_db_and_tables, get_session

models.folder.FolderRead.update_forward_refs(
    ContactRead=models.contact.ContactRead, UserRead=models.user.UserRead
)

router = APIRouter(prefix="/folder", tags=["folder"])


@router.post("/", response_model=models.folder.FolderRead)
def add_folder(
    folder: models.folder.FolderCreate, session: Session = Depends(get_session)
):
    db_user = session.get(models.user.User, folder.user_id)
    if db_user is None:
        raise HTTPException(404, "User not found")
    db_folder = models.folder.Folder.validate(folder)
    session.add(db_folder)
    session.commit()
    session.refresh(db_folder)
    return db_folder
