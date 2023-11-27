from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel, create_engine

from .relations import FolderContactLink

if TYPE_CHECKING:
    from .folder import Folder
    from .user import User


class ContactBase(SQLModel):
    name: Optional[str] = Field(default=None)
    email: str
    user_id: int


class Contact(ContactBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="contacts")
    folders: List["Folder"] = Relationship(
        back_populates="contacts", link_model=FolderContactLink
    )


class ContactRead(ContactBase):
    id: int


class ContactCreate(ContactBase):
    folder_ids: List[int] = []
