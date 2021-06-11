from logging import error
from typing import List
from fastapi import APIRouter, WebSocket, HTTPException, status
from fastapi.param_functions import Query
from starlette.websockets import WebSocketDisconnect
from security.auth import get_current_user, User 
from models import store_message, Message


prefix = "/api"
router = APIRouter(prefix=prefix)


# broadcast chatroom
class ChatRoom:
    def __init__(self, roomID):
        self.chatConnections : List[WebSocket] = []
        self.roomId : str

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.chatConnections.append(websocket)

    async def broadcast(self, message: Message):
        messageDict = message.getJSONSafeMapping()
        
        # remove items before we send it over the network for privacy and bandwidth
        messageDict.pop("chatroomID")
        messageDict["user"].pop("full_name")

        # send message to all websockets in connection pool
        for connection in self.chatConnections:
            await connection.send_json(messageDict)
        
    def disconnect(self, websocket):
        self.chatConnections.remove(websocket)


globalChat = ChatRoom(roomID=1)

# weird prefix workaround
# api router doens't prefix websockets
# probably will be fixed later https://github.com/tiangolo/fastapi/pull/3280
@router.websocket(f"{prefix}/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    # TODO Multiple Chatrooms
    chatroomID = 1

    # remove hashed password from data we are going to send
    userWithTooManyDetails = await get_current_user(token)
    user : User =  User(**userWithTooManyDetails.dict())
    if not user:
        # TODO Figure out if httpsexceptions are the way to handle bad auth for websockets
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",)
        
    await globalChat.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = store_message(user, data, chatroomID)
            await globalChat.broadcast(message)
    except WebSocketDisconnect:
        globalChat.disconnect(websocket)

