from fastapi import APIRouter
from app.api.sys import router as sys_router
from app.api.ws_test import router as ws_router
router = APIRouter()
router.include_router(sys_router)
router.include_router(ws_router)
