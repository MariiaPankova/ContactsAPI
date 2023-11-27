from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine

if TYPE_CHECKING:
    from .contact import Contact
    from .folder import Folder


class UserBase(SQLModel):
    email: str = Field(index=True)
    password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    folders: List["Folder"] = Relationship(back_populates="user")
    contacts: List["Contact"] = Relationship(back_populates="user")


class UserRead(UserBase):
    id: int

    password: str = Field(exclude=True)


class UserCreate(UserBase):
    pass


class UserUpdate(SQLModel):
    email: Optional[str] = None
    password: Optional[str] = None
