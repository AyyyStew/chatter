from os import name
from os.path import isfile

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from api import chat
from security import auth
from website import site

app = FastAPI()
app.include_router(auth.router)
app.include_router(site.router)
app.include_router(chat.router)

app.mount("/static", StaticFiles(directory="./static/", html=True), name="static")




