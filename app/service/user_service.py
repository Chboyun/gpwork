from typing import Any

from app.crud.user_dao import user_dao
from app.model.all_model import User
from app.schema.user import UserCreateParam, UserVerifyParam, UserUpdateParam
from database.db_mysql import async_db_session
from common.response.response_schema import ResponseModel, response_base


class UserService:
    @staticmethod
    async def get(*, user_id: int) -> User:
        async with async_db_session() as db:
            user = await user_dao.get_by_id(db, user_id)
            return user

    @staticmethod
    async def create(user: UserCreateParam) -> User:
        async with async_db_session.begin() as db:
            return await user_dao.create(db, user)

    @staticmethod
    async def delete(user_id: int):
        async with async_db_session.begin() as db:
            return await user_dao.delete(db, user_id)

    @staticmethod
    async def update(user: UserUpdateParam):
        async with async_db_session.begin() as db:
            return await user_dao.update(db, user)

    @staticmethod
    async def get_all():
        async with async_db_session() as db:
            return await user_dao.get_all(db)

    @staticmethod
    async def get_by_username(username: str):
        async with async_db_session() as db:
            return await user_dao.get_by_username(db, username)

    @staticmethod
    async def getUserVerifyParam(username: str) -> UserVerifyParam:
        async with async_db_session() as db:
            return await user_dao.get_user_verify_by_username(db, username)

