from fastapi import APIRouter
from app.service.label_service import LabelService
from common.response.response_schema import ResponseModel, response_base
from app.schema.label import LabelCreateParam, LabelUpdateParam

router = APIRouter()


@router.get("/all", response_model=ResponseModel, dependencies=[])
async def get_label() -> ResponseModel:
    data = await LabelService.get_all()
    return await response_base.success(data=data)


@router.post("/add", response_model=ResponseModel)
async def add_label(params: LabelCreateParam) -> ResponseModel:
    data = await LabelService.create(params)
    return await response_base.success(data=data)


@router.post("/update", response_model=ResponseModel)
async def update_label(params: LabelUpdateParam) -> ResponseModel:
    data = await LabelService.update(params)
    return await response_base.success(data=data)


@router.delete("/delete", response_model=ResponseModel)
async def delete_label(params: int) -> ResponseModel:
    data = await LabelService.delete(params)
    return await response_base.success(data=data)


@router.post("/add_label_to_kl", response_model=ResponseModel)
async def add_label_to_kl(label_id: int, kl_id: int) -> ResponseModel:
    data = await LabelService.add_label_to_kl(label_id, kl_id)
    return await response_base.success(data=data)


@router.post("/remove_label_from_kl", response_model=ResponseModel)
async def remove_label_from_kl(label_id: int, kl_id: int) -> ResponseModel:
    data = await LabelService.remove_label_from_kl(label_id, kl_id)
    return await response_base.success(data=data)




