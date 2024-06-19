from fastapi import APIRouter

from app.schema.user import UserCreateParam, UserUpdateParam
from app.service.user_service import UserService
from common.response.response_schema import ResponseModel, response_base


router = APIRouter()


@router.get("/user_id/{user_id}",
            response_model=ResponseModel,
            summary="根据用户ID获取用户信息")
async def get_user(user_id: int) -> ResponseModel:
    data = await UserService.get(user_id=user_id)
    return await response_base.success(data=data)


@router.post("/create", response_model=ResponseModel)
async def create_user(params: UserCreateParam) -> ResponseModel:
    data = await UserService.create(params)
    return await response_base.success(data=data)


@router.post("/delete/{user_id}", response_model=ResponseModel)
async def delete_user(user_id: int) -> ResponseModel:
    data = await UserService.delete(user_id)
    return await response_base.success(data=data)


@router.post("/update", response_model=ResponseModel)
async def update_user(params: UserUpdateParam) -> ResponseModel:
    data = await UserService.update(params)
    return await response_base.success(data=data)


@router.get("/all", response_model=ResponseModel)
async def get_all_user() -> ResponseModel:
    print('get_all_user-------------')
    data = await UserService.get_all()
    return await response_base.success(data=data)


@router.get("/user_name/{username}", response_model=ResponseModel)
async def get_user_by_username(username: str) -> ResponseModel:
    data = await UserService.get_by_username(username)
    return await response_base.success(data=data)

