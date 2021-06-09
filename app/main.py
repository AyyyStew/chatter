from os import name
from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request


from security import auth

app = FastAPI()
app.include_router(auth.router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
