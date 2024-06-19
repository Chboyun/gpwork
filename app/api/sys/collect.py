from fastapi import APIRouter

from app.crud.collect_dao import CollectParam
from app.service.kl_service import KLService
from common.response.response_schema import ResponseModel, response_base
from app.schema.knowledge import KLSearchParam, KLCreateParam, KLUpdateContentParam
from app.service.collect_service import CollectService
router = APIRouter()


@router.post("/add", response_model=ResponseModel)
async def add_collect(params: CollectParam) -> ResponseModel:
    data = await CollectService.add_collect(params)
    return await response_base.success(data=data)


@router.post("/remove_by_collect_id", response_model=ResponseModel)
async def remove_by_collect_id(collect_id: int, user_id: int) -> ResponseModel:
    data = await CollectService.remove_collect_by_collect_id(collect_id, user_id)
    return await response_base.success(data=data)


@router.post("/remove_by_kl_id", response_model=ResponseModel)
async def remove_by_kl_id(kl_id: int, user_id: int) -> ResponseModel:
    data = await CollectService.remove_collect_by_kl_id(kl_id, user_id)
    return await response_base.success(data=data)


@router.get("/list", response_model=ResponseModel)
async def get_collect_list(user_id: int) -> ResponseModel:
    data = await CollectService.get_collect_list(user_id)
    return await response_base.success(data=data)


