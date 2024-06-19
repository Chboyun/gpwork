from typing import Union

from fastapi import FastAPI
from fastapi.params import Query
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse
from fastapi import FastAPI, File, UploadFile
from core.conf import settings
from app.api.router import router as test_router
from common.exception.exception_handler import register_exception

# app.include_router(test_router)
# register_exception(app)
from core.registrar import register_app

app = register_app()
