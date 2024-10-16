from sqlmodel import Field, Relationship, SQLModel

from models.directories import Directory

class Email(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    emails: Directory = Relationship(back_populates='emails')