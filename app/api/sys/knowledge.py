from fastapi import APIRouter
from app.service.kl_service import KLService
from common.response.response_schema import ResponseModel, response_base
from app.schema.knowledge import KLSearchParam, KLCreateParam, KLUpdateContentParam

router = APIRouter()


@router.post("/search", response_model=ResponseModel)
async def search(params: KLSearchParam) -> ResponseModel:
    data = await KLService.search(params)
    return await response_base.success(data=data)


@router.post("/create", response_model=ResponseModel)
async def create(params: KLCreateParam) -> ResponseModel:
    data = await KLService.create(params)
    return await response_base.success(data=data)


@router.post("/updateContent", response_model=ResponseModel)
async def update_content(params: KLUpdateContentParam) -> ResponseModel:
    data = await KLService.change_content(params)
    return await response_base.success(data=data)


@router.get("/details/{kl_id}", response_model=ResponseModel)
async def details(kl_id: int) -> ResponseModel:
    data = await KLService.getKlDetails(kl_id)
    return await response_base.success(data=data)


@router.post("/like/{kl_id}", response_model=ResponseModel)
async def like(kl_id: int) -> ResponseModel:
    data = await KLService.like_change(kl_id, 1)
    return await response_base.success(data=data)


@router.post("/cancel_like/{kl_id}", response_model=ResponseModel)
async def like(kl_id: int) -> ResponseModel:
    data = await KLService.like_change(kl_id, -1)
    return await response_base.success(data=data)


@router.post("/dislike/{kl_id}", response_model=ResponseModel)
async def dislike(kl_id: int) -> ResponseModel:
    data = await KLService.dislike_change(kl_id, 1)
    return await response_base.success(data=data)


@router.post("/cancel_dislike/{kl_id}", response_model=ResponseModel)
async def dislike(kl_id: int) -> ResponseModel:
    data = await KLService.dislike_change(kl_id, -1)
    return await response_base.success(data=data)


@router.post("/state/offline/{kl_id}", response_model=ResponseModel)
async def offline(kl_id: int) -> ResponseModel:
    data = await KLService.state_change(kl_id, 3)
    return await response_base.success(data=data)


@router.post("/state/online/{kl_id}", response_model=ResponseModel)
async def online(kl_id: int) -> ResponseModel:
    data = await KLService.state_change(kl_id, 2)
    return await response_base.success(data=data)


@router.post("/state/refuse/{kl_id}", response_model=ResponseModel)
async def refuse(kl_id: int) -> ResponseModel:
    data = await KLService.state_change(kl_id, 1)
    return await response_base.success(data=data)
