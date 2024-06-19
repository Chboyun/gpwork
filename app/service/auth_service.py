#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import Request
from fastapi.security import HTTPBasicCredentials
from starlette.background import BackgroundTask, BackgroundTasks

# from backend.app.admin.conf import admin_settings
from app.crud.user_dao import user_dao
from app.model.all_model import User
from app.schema.token import GetLoginToken, GetNewToken

from app.schema.user import UserVerifyParam
from common.enums import LoginLogStatusType
from common.exception import errors
from common.response.response_code import CustomErrorCode
from common.security.jwt import (
    create_access_token,
    create_new_token,
    create_refresh_token,
    get_token,
    jwt_decode,
    password_verify,
)
from core.conf import settings
from database.db_mysql import async_db_session
from database.db_redis import redis_client
from utils.timezone import timezone


class AuthService:
    @staticmethod
    async def swagger_login(obj: HTTPBasicCredentials) -> tuple[str, User]:
        async with async_db_session.begin() as db:
            current_user = await user_dao.get_user_verify_by_username(db, obj.username)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            elif obj.password != current_user.password:
                raise errors.AuthorizationError(msg='密码错误')

            access_token, _ = await create_access_token(str(current_user.user_id))
            return access_token, current_user

    @staticmethod
    async def login(*, request: Request, obj: UserVerifyParam) -> GetLoginToken:
        async with async_db_session.begin() as db:
            try:
                current_user = await user_dao.get_user_verify_by_username(db, obj.username)
                if not current_user:
                    raise errors.NotFoundError(msg='用户不存在')
                elif obj.password != current_user.password:
                    raise errors.AuthorizationError(msg='密码错误')

                access_token, access_token_expire_time = await create_access_token(
                    str(current_user.user_id)
                )
                refresh_token, refresh_token_expire_time = await create_refresh_token(
                    str(current_user.user_id), access_token_expire_time
                )

            except errors.NotFoundError as e:
                raise errors.NotFoundError(msg=e.msg)
            except (errors.AuthorizationError, errors.CustomError) as e:
                raise errors.AuthorizationError(msg=e.msg)
            except Exception as e:
                raise e
            else:
                data = GetLoginToken(
                    access_token=access_token,
                    refresh_token=refresh_token,
                    access_token_expire_time=access_token_expire_time,
                    refresh_token_expire_time=refresh_token_expire_time,
                    user=current_user,  # type: ignore
                )
                return data

    @staticmethod
    async def new_token(*, request: Request, refresh_token: str) -> GetNewToken:
        user_id = await jwt_decode(refresh_token)
        if request.user.user_id != user_id:
            raise errors.TokenError(msg='刷新 token 无效')
        async with async_db_session() as db:
            current_user = await user_dao.get_by_id(db, user_id)
            if not current_user:
                raise errors.NotFoundError(msg='用户不存在')
            current_token = await get_token(request)
            (
                new_access_token,
                new_refresh_token,
                new_access_token_expire_time,
                new_refresh_token_expire_time,
            ) = await create_new_token(
                str(current_user.user_id), current_token, refresh_token
            )
            data = GetNewToken(
                access_token=new_access_token,
                access_token_expire_time=new_access_token_expire_time,
                refresh_token=new_refresh_token,
                refresh_token_expire_time=new_refresh_token_expire_time,
            )
            return data

    @staticmethod
    async def logout(*, request: Request) -> None:
        prefix = f'{settings.TOKEN_REDIS_PREFIX}:{request.user.user_id}:'
        await redis_client.delete_prefix(prefix)


auth_service = AuthService()
