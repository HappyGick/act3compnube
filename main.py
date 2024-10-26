from typing import Annotated
from dotenv import load_dotenv
from sqlmodel import select

load_dotenv()

from fastapi import FastAPI, Path, Request
from fastapi.responses import JSONResponse
from starlette.responses import RedirectResponse
from db import SessionDep, init_db

from models import Email, Directory

from pydantic import BaseModel
from sqlalchemy import exc

import re

class DirectoryModel(BaseModel):
    name: str
    emails: list[str]

class PartialDirectoryModel(BaseModel):
    name: str | None = None
    emails: list[str] | None = None

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return RedirectResponse('/status')

@app.get('/status')
def root():
    return 'pong'

@app.get('/directories')
def root(session: SessionDep, req: Request, page: int = 0):
    statement = select(Directory).offset(page * 10).limit(10)
    results = session.exec(statement)
    r_list = []
    for r in results:
        r_list.append({
            'id': r.id,
            'name': r.name,
            'emails': list(map(lambda e: e.email, r.emails))
        })
    return {
        'count': len(r_list),
        'next': str(req.base_url) + 'directories?page=' + str(page + 1),
        'previous': str(req.base_url) + 'directories?page=' + str(page - 1) if page > 0 else None,
        'results': r_list
    }

@app.post('/directories')
def root(session: SessionDep, directory: DirectoryModel):
    for e in directory.emails:
        if len(re.findall('^[\\w\-\\.]+@([\\w\-]+\\.)+[\\w\-]{2,4}$', e)) != 1:
            return JSONResponse('Error: ' + e + ' is not an email.', status_code=400)

    try:
        d = Directory(name=directory.name)
        session.add(d)
        session.commit()
        session.refresh(d)
        emails= list(map(lambda e: Email(email=e, directory_id=d.id), directory.emails))
        session.add_all(emails)
        session.commit()
        session.refresh(d)
    except exc.IntegrityError:
        session.rollback()
        return JSONResponse('Error: directory ' + directory.name + ' already exists', status_code=409)
    return {
        'id': d.id,
        'name': d.name,
        'emails': list(map(lambda e: e.email, d.emails))
    }

@app.get('/directories/{obj_id}')
def root(session: SessionDep, obj_id: Annotated[int, Path(title="El ID del objeto a leer")]):
    q = select(Directory).where(Directory.id == obj_id)
    r = session.exec(q)
    try:
        d = r.one()
        return {
            'id': d.id,
            'name': d.name,
            'emails': list(map(lambda e: e.email, d.emails))
        }
    except exc.NoResultFound:
        return JSONResponse('Directory with ID ' + str(obj_id) + ' not found.', status_code=404)

@app.put('/directories/{obj_id}')
def root(session: SessionDep, obj_id: Annotated[int, Path(title="El ID del objeto a modificar")], directory: DirectoryModel):
    for e in directory.emails:
        if len(re.findall('^[\\w\-\\.]+@([\\w\-]+\\.)+[\\w\-]{2,4}$', e)) != 1:
            return JSONResponse('Error: ' + e + ' is not an email.', status_code=400)
    
    q = select(Directory).where(Directory.id == obj_id)
    r = session.exec(q)
    try:
        d: Directory = r.one()
        d.name = directory.name,
        for e in d.emails:
            session.delete(e)
        session.commit()
        emails= list(map(lambda e: Email(email=e, directory_id=d.id), directory.emails))
        session.add_all(emails)
        session.add(d)
        session.commit()
        session.refresh(d)
        return {
            'id': d.id,
            'name': d.name,
            'emails': list(map(lambda e: e.email, d.emails))
        }
    except exc.NoResultFound:
        session.rollback()
        return JSONResponse('Directory with ID ' + str(obj_id) + ' not found.', status_code=404)
    except exc.IntegrityError:
        session.rollback()
        return JSONResponse('Error: directory ' + directory.name + ' already exists', status_code=409)

@app.patch('/directories/{obj_id}')
def root(session: SessionDep, obj_id: Annotated[int, Path(title="El ID del objeto a modificar parcialmente")], directory: PartialDirectoryModel):
    if directory.emails != None:
        for e in directory.emails:
            if len(re.findall('^[\\w\-\\.]+@([\\w\-]+\\.)+[\\w\-]{2,4}$', e)) != 1:
                return JSONResponse('Error: ' + e + ' is not an email.', status_code=400)
    
    q = select(Directory).where(Directory.id == obj_id)
    r = session.exec(q)
    try:
        d: Directory = r.one()
        if directory.name != None:
            d.name = directory.name,
        if directory.emails != None:
            emails= list(map(lambda e: Email(email=e, directory_id=d.id), directory.emails))
            session.add_all(emails)
        session.add(d)
        session.commit()
        session.refresh(d)
        return {
            'id': d.id,
            'name': d.name,
            'emails': list(map(lambda e: e.email, d.emails))
        }
    except exc.NoResultFound:
        session.rollback()
        return JSONResponse('Directory with ID ' + str(obj_id) + ' not found.', status_code=404)
    except exc.IntegrityError:
        session.rollback()
        return JSONResponse('Error: directory ' + directory.name + ' already exists', status_code=409)

@app.delete('/directories/{obj_id}')
def root(session: SessionDep, obj_id: Annotated[int, Path(title="El ID del objeto a borrar")]):
    q = select(Directory).where(Directory.id == obj_id)
    r = session.exec(q)
    try:
        d = r.one()
        session.delete(d)
        session.commit()
        return 'Success'
    except exc.NoResultFound:
        session.rollback()
        return JSONResponse('Directory with ID ' + str(obj_id) + ' not found.', status_code=404)