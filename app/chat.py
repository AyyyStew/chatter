from logging import error
from fastapi import APIRouter, WebSocket, HTTPException, status
from fastapi.param_functions import Query
from security.auth import get_current_user, User 


prefix = "/api"
router = APIRouter(prefix=prefix)

# weird prefix workaround
# api router doens't prefix websockets
# probably will be fixed later https://github.com/tiangolo/fastapi/pull/3280
@router.websocket(f"{prefix}/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    print(token)
    user : User =  await get_current_user(token)
    if user:
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f"Message text was: {data}")
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",)

