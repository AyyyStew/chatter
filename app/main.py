from os import name
from os.path import isfile

from fastapi import FastAPI, WebSocket
from fastapi.staticfiles import StaticFiles

from security import auth
from website import site

app = FastAPI()
app.include_router(auth.router)
app.include_router(site.router)

app.mount("/static", StaticFiles(directory="./static/", html=True), name="static")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text(f"Message text was: {data}")


