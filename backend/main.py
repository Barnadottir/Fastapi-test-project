# main.py

from fastapi import FastAPI, Request
from middleware import Auth

app = FastAPI()

@app.get("/open-data")
async def root():
    return {"message": "Hello, FastAPI on Mac!"}

@app.get("/secure-data")
@Auth('token')
async def root(request: Request):
    my_header = request.headers.get('my-header')
    return {"message": "successfully logged in!"}

@app.post('/login')

@Login
async def login(request: Request):
    password, username = request.password, request.username
