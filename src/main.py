from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from src import models
from src.app import routers
from src.infrastructure.database import create_db_and_tables, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(routers.contact_router)
app.include_router(routers.folder_router)
app.include_router(routers.user_router)
