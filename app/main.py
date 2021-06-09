from os import name
from os.path import isfile
from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

import chat
import website
from security import auth

app = FastAPI()
app.include_router(auth.router)
app.include_router(website.router)
app.include_router(chat.router)

app.mount("/static", StaticFiles(directory="./static/", html=True), name="static")



