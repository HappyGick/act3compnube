from fastapi import FastAPI
from starlette.responses import RedirectResponse

from db import SessionDep, init_db

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
def root(session: SessionDep):
    pass

@app.post('/directories')
def root(session: SessionDep):
    pass

@app.get('/directories/:id')
def root(session: SessionDep):
    pass

@app.put('/directories/:id')
def root(session: SessionDep):
    pass

@app.patch('/directories/:id')
def root(session: SessionDep):
    pass

@app.delete('/directories/:id')
def root(session: SessionDep):
    pass