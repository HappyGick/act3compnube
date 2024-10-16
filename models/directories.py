from sqlmodel import Field, SQLModel, Relationship

from models.emails import Email

class Directory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    emails:list['Email'] = Relationship(back_populates='directory', cascade_delete=True)
