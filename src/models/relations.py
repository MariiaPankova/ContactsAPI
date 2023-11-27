from typing import Optional

from sqlmodel import Field, SQLModel


class FolderContactLink(SQLModel, table=True):
    folder_id: Optional[int] = Field(
        default=None, foreign_key="folder.id", primary_key=True
    )
    contact_id: Optional[int] = Field(
        default=None, foreign_key="contact.id", primary_key=True
    )
