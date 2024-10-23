from sqlmodel import Field, SQLModel, Relationship

class Directory(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    emails:list['Email'] = Relationship(back_populates='directory', cascade_delete=True)

class Email(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True)
    directory_id: int | None = Field(default=None, foreign_key="directory.id")
    directory: Directory | None = Relationship(back_populates='emails')
