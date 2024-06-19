from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_crud_plus import CRUDPlus
from app.model.all_model import User
from app.schema.user import UserCreateParam, UserDetails, UserUpdateParam, UserVerifyParam
from common.exception import errors
from common.response.response_schema import ResponseModel, response_base
from utils.serializers import select_list_serialize


class CRUDUser:
    def __init__(self, model):
        self.model = model

    async def get_by_id(self, db: AsyncSession, user_id: int) -> UserDetails:
        stat = select(self.model).filter(self.model.user_id == user_id)
        row = (await db.scalars(stat)).first()
        if not row:
            raise errors.NotFoundError(msg='用户不存在')

        data = UserDetails.from_orm(row)
        return data

    async def get_by_username(self, db: AsyncSession, username: str) -> UserDetails:
        stat = select(self.model).filter(self.model.username == username)
        row = (await db.scalars(stat)).first()
        if not row:
            raise errors.NotFoundError(msg='用户不存在')

        data = UserDetails.from_orm(row)
        return data

    async def get_user_verify_by_username(self, db: AsyncSession, username: str) -> UserVerifyParam:
        stat = select(self.model).filter(self.model.username == username)
        row = (await db.scalars(stat)).first()
        if not row:
            raise errors.NotFoundError(msg='用户不存在')

        data = UserVerifyParam.from_orm(row)
        return data


    async def create(self, db: AsyncSession, user: UserCreateParam) -> UserDetails:
        db_user = self.model(**user.dict())
        db.add(db_user)
        await db.flush()
        await db.refresh(db_user)
        data = UserDetails.from_orm(await db.get(User, db_user.user_id))
        await db.commit()
        return data

    async def update(self, db: AsyncSession, user: UserUpdateParam) -> UserDetails:
        stat = select(self.model).filter(self.model.user_id == user.user_id)
        data = await db.scalars(stat)
        user1 = data.first()
        if not user1:
            raise errors.NotFoundError(msg='用户不存在')
        if user.username:
            user1.username = user.username
        if user.password:
            user1.password = user.password
        await db.flush()
        await db.refresh(user1)
        data = UserDetails.from_orm(await db.get(User, user1.user_id))
        await db.commit()
        return data

    async def delete(self, db: AsyncSession, user_id: int) -> None:
        stat = select(self.model).filter(self.model.user_id == user_id)
        data = await db.scalars(stat)
        user = data.first()
        if not user:
            raise errors.NotFoundError(msg='删除一个不存在的用户')

        await db.delete(user)
        await db.commit()

    async def get_all(self, db: AsyncSession) -> list[UserDetails]:
        result = (await db.scalars(select(self.model))).all()
        rows = await select_list_serialize(result)
        data = [UserDetails.from_orm(row) for row in rows]
        return data


user_dao = CRUDUser(User)
