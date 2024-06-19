from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload
from app.model.all_model import Collect
from app.model.all_model import Knowledge, Label, KlLabel, User, Annex
from sqlalchemy import and_, asc, or_, select
from app.schema.knowledge import KLSearchParam, KLUpdateParam, KLCreateParam, KLRead, KlDetails
from app.schema.user import UserDetails
from common.exception import errors
from utils.serializers import select_as_dict
from common.schema import SchemaBase


class CollectParam(SchemaBase):
    user_id: int
    kl_id: int


class CollectRead(CollectParam):
    collect_id: int
    # kl: KLRead
    create_time: datetime
    update_time: datetime
    model_config = ConfigDict(from_attributes=True)



class CollectList(UserDetails):
    collect: list[CollectRead]
    model_config = ConfigDict(from_attributes=True)


class CRUDCollect:
    def __init__(self, model):
        self.model = model

    async def add_collect(self, db: AsyncSession, param: CollectParam) -> CollectRead:
        db_collect = self.model(**param.dict())
        db.add(db_collect)
        await db.flush()
        await db.refresh(db_collect)
        data = CollectRead.from_orm(await db.get(Collect, db_collect.collect_id))
        await db.commit()
        return data

    async def remove_collect_by_collect_id(self, db: AsyncSession, collect_id: int, user_id: int):
        stat = select(self.model).filter(self.model.collect_id == collect_id, self.model.user_id == user_id)
        data = await db.scalars(stat)
        db_collect = data.first()
        if not db_collect:
            raise errors.NotFoundError(msg='删除一个不存在的收藏')
        await db.delete(db_collect)
        await db.commit()

    async def remove_collect_by_kl_id(self, db: AsyncSession, kl_id: int, user_id: int):
        stat = select(self.model).filter(self.model.kl_id == kl_id, self.model.user_id == user_id)
        data = await db.scalars(stat)
        db_collect = data.first()
        if not db_collect:
            raise errors.NotFoundError(msg='删除一个不存在的收藏')
        await db.delete(db_collect)
        await db.commit()

    async def get_collect_list(self, db: AsyncSession, user_id: int) -> CollectList:
        stat = (select(User)
                .options(joinedload(User.collect))
                .where(User.user_id == user_id)
                )
        result = (await db.scalars(stat)).first()
        return CollectList.from_orm(result)


collect_dao = CRUDCollect(Collect)
