import json

from fastapi import APIRouter, Header
from pydantic import BaseModel
from starlette.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Depends, Query, Request

from app.crud.kl_dao import kl_dao
from app.crud.user_dao import user_dao
from app.schema.user import UserDetails
from common.response.response_schema import ResponseModel
from common.security import jwt
from common.security.jwt import DependsJwtAuth
from database.db_mysql import async_db_session

router = APIRouter(prefix='/ws', tags=['WebSocket'])


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, client_id: int):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            await websocket.send_text(message)

    async def send_msg_to_user(self, message: str, sender: int, receiver: int):
        if sender in self.active_connections and receiver in self.active_connections:
            receiver_websocket = self.active_connections[receiver]
            await receiver_websocket.send_text(message)


manager = ConnectionManager()


@router.websocket("/link")
async def websocket_endpoint(
        websocket: WebSocket,
        token: str,
):
    user_id = await jwt.jwt_decode(token)
    try:
        await manager.connect(user_id, websocket)
    except WebSocketDisconnect as e:
        manager.disconnect(user_id)


@router.get("/all_online", response_model=ResponseModel, summary='获取所有在线用户')
async def get_all_online():
    kys = manager.active_connections.keys()
    data: list[UserDetails] = []
    for ky in kys:
        async with async_db_session() as db:
            user = await user_dao.get_by_id(db, ky)
            data.append(user)
    return ResponseModel(data=data)


class ShareKl(BaseModel):
    user_id: int
    kl_id: int


@router.post("/send_msg", response_model=ResponseModel, summary='分享知识', dependencies=[DependsJwtAuth])
async def send_msg(obj: ShareKl, request: Request):
    msg = json.dumps(obj.dict())
    await manager.send_msg_to_user(msg, request.user.user_id, obj.user_id)
    return ResponseModel(data='发送成功')
