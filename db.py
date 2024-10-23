import os
from typing import Annotated
from fastapi import Depends

from sqlmodel import create_engine, SQLModel, Session

DATABASE_URL = "postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}".format(POSTGRES_PASSWORD= os.environ.get("POSTGRES_PASSWORD"),
POSTGRES_USER= os.environ.get("POSTGRES_USER"),
POSTGRES_HOST= os.environ.get("POSTGRES_HOST"),
POSTGRES_PORT= os.environ.get("POSTGRES_PORT"),
POSTGRES_DB= os.environ.get("POSTGRES_DB"))
engine = create_engine(DATABASE_URL, echo=True)


def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]