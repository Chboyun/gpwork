from fastapi import APIRouter

from app.schema.library import LibraryCreateParam, LibraryUpdateParam
from app.service.label_service import LabelService
from app.service.library_service import LibraryService
from common.response.response_schema import ResponseModel, response_base
from app.schema.label import LabelCreateParam, LabelUpdateParam

router = APIRouter()


@router.get("/all", response_model=ResponseModel)
async def get_library() -> ResponseModel:
    data = await LibraryService.get_all()
    return await response_base.success(data=data)


@router.post("/add", response_model=ResponseModel)
async def add_library(params: LibraryCreateParam) -> ResponseModel:
    data = await LibraryService.create(params)
    return await response_base.success(data=data)


@router.post("/delete/{library_id}", response_model=ResponseModel)
async def delete_library(library_id: int) -> ResponseModel:
    data = await LibraryService.delete(library_id)
    return await response_base.success(data=data)


@router.post("/update", response_model=ResponseModel)
async def update_library(params: LibraryUpdateParam) -> ResponseModel:
    data = await LibraryService.update(params)
    return await response_base.success(data=data)


@router.get("/{library_id}", response_model=ResponseModel)
async def get_kl_in_library(library_id: int) -> ResponseModel:
    data = await LibraryService.get_kl_in_library(library_id)
    return await response_base.success(data=data)


@router.post("/add_kl/{library_id}/{kl_id}", response_model=ResponseModel)
async def add_kl_to_library(library_id: int, kl_id: int) -> ResponseModel:
    data = await LibraryService.add_kl_to_library(library_id, kl_id)
    return await response_base.success(data=data)


@router.post("/remove_kl/{library_id}/{kl_id}", response_model=ResponseModel)
async def remove_kl_from_library(library_id: int, kl_id: int) -> ResponseModel:
    data = await LibraryService.remove_kl_from_library(library_id, kl_id)
    return await response_base.success(data=data)