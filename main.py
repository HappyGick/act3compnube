from fastapi import FastAPI
from starlette.responses import RedirectResponse

from db import init_db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def root():
    return RedirectResponse('/status')

@app.get('/status')
def root():
    pass

@app.get('/directories')
def root():
    pass

@app.post('/directories')
def root():
    pass

@app.get('/directories/:id')
def root():
    pass

@app.put('/directories/:id')
def root():
    pass

@app.patch('/directories/:id')
def root():
    pass

@app.delete('/directories/:id')
def root():
    pass