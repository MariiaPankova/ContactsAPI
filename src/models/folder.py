from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine

from .relations import FolderContactLink

if TYPE_CHECKING:
    from .contact import Contact, ContactRead
    from .user import User, UserRead


class FolderBase(SQLModel):
    name: str
    user_id: int


class Folder(FolderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="folders")
    contacts: List["Contact"] = Relationship(
        back_populates="folders", link_model=FolderContactLink
    )


class FolderCreate(FolderBase):
    pass


class FolderRead(FolderBase):
    id: int
    contacts: List["ContactRead"] = []
    user: Optional["UserRead"] = None
