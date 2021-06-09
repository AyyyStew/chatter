import re
from fastapi import APIRouter, WebSocket, Depends
from fastapi.param_functions import Query
from security.auth import get_current_active_user, User


prefix = "/api"
router = APIRouter(prefix=prefix)

# weird prefix workaround
# api router doens't prefix websockets
# probably will be fixed later https://github.com/tiangolo/fastapi/pull/3280
@router.websocket(f"{prefix}/chat")
async def websocket_endpoint(websocket: WebSocket):
    # print(token)
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(data)
        await websocket.send_text(f"Message text was: {data}")

