#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from app.api.router import router as router_test
from common.exception.exception_handler import register_exception
from core.conf import settings
from core.path_conf import STATIC_DIR
from database.db_redis import redis_client
# from backend.database.db_mysql import create_table
# from backend.database.db_redis import redis_client
from middleware.jwt_auth_middleware import JwtAuthMiddleware
# from middleware.opera_log_middleware import OperaLogMiddleware
from utils.serializers import MsgSpecJSONResponse


@asynccontextmanager
async def register_init(app: FastAPI):
    """
    启动初始化

    :return:
    """
    # 连接 redis
    await redis_client.open()

    yield

    # 关闭 redis 连接
    await redis_client.close()


def register_app():
    # FastAPI
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        default_response_class=MsgSpecJSONResponse,
        lifespan=register_init,
    )

    # 静态文件
    register_static_file(app)

    # 中间件
    register_middleware(app)

    # 路由
    register_router(app)

    # 全局异常处理
    register_exception(app)

    return app


def register_static_file(app: FastAPI):
    """
    静态文件交互开发模式, 生产使用 nginx 静态资源服务

    :param app:
    :return:
    """
    if settings.STATIC_FILES:
        import os

        from fastapi.staticfiles import StaticFiles

        if not os.path.exists(STATIC_DIR):
            os.mkdir(STATIC_DIR)
        app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')


def register_middleware(app: FastAPI):
    """
    中间件，执行顺序从下往上

    :param app:
    :return:
    """
    # Opera log
    # app.add_middleware(OperaLogMiddleware)
    # JWT auth, required
    app.add_middleware(
        AuthenticationMiddleware, backend=JwtAuthMiddleware(), on_error=JwtAuthMiddleware.auth_exception_handler
    )
    # CORS: Always at the end
    if settings.MIDDLEWARE_CORS:
        from fastapi.middleware.cors import CORSMiddleware

        app.add_middleware(
            CORSMiddleware,
            allow_origins=['*'],
            allow_credentials=True,
            allow_methods=['*'],
            allow_headers=['*'],
        )


def register_router(app: FastAPI):
    # API
    app.include_router(router_test)


