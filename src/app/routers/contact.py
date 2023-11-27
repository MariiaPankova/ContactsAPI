from contextlib import asynccontextmanager
from typing import List

from fastapi import APIRouter, Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from src import models
from src.infrastructure.database import create_db_and_tables, get_session

router = APIRouter(prefix="/contact", tags=["contact"])


@router.post("/", response_model=models.contact.ContactRead)
def add_contact(
    contact: models.contact.ContactCreate, session: Session = Depends(get_session)
):
    db_user = session.get(models.user.User, contact.user_id)
    if db_user is None:
        raise HTTPException(404, "User not found")
    q = select(models.folder.Folder).where(
        models.folder.Folder.id.in_(contact.folder_ids)
    )
    db_folders = session.exec(q).all()
    db_folder_ids = {folder.id for folder in db_folders}
    if not_found := set(contact.folder_ids).difference(db_folder_ids):
        raise HTTPException(404, f"No such folders: {not_found}")
    db_contact = models.contact.Contact.validate(contact)
    db_contact.folders = db_folders

    session.add(db_contact)
    session.commit()
    session.refresh(db_contact)
    return db_contact
