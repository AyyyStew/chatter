from logging import error
from typing import List
from fastapi import APIRouter, WebSocket, HTTPException, status
from fastapi.param_functions import Query
from security.auth import get_current_user, User 
from models import store_message, Message


prefix = "/api"
router = APIRouter(prefix=prefix)


# pub sub chat room
class ChatRoom:
    def __init__(self, roomID):
        self.chatConnections : List[WebSocket] = []
        self.roomId : str

    def subscribe(self, websocket: WebSocket):
        self.chatConnections.append(websocket)

    async def publish(self, message: Message):
        messageWithoutChatroomID = message.getJSONSafeMapping()
        messageWithoutChatroomID.pop("chatroomID")
        for connection in self.chatConnections:
            await connection.send_json(messageWithoutChatroomID)
        
        # return True

globalChat = ChatRoom(roomID=1)

# weird prefix workaround
# api router doens't prefix websockets
# probably will be fixed later https://github.com/tiangolo/fastapi/pull/3280
@router.websocket(f"{prefix}/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    print(token)
    # TODO Multiple Chatrooms
    chatroomID = 1

    # remove hashed password from data we are going to send
    userWithTooManyDetails = await get_current_user(token)
    user : User =  User(**userWithTooManyDetails.dict())
    
    # if authenticated
    if user:
        globalChat.subscribe(websocket)
        await websocket.accept()
        while True:
            data = await websocket.receive_text()
            message : Message = store_message(user, data, chatroomID)
            await globalChat.publish(message)
    else:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials",)

