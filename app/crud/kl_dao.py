from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.model.all_model import Knowledge, Label, KlLabel, User, Annex
from sqlalchemy import and_, asc, or_, select
from app.schema.knowledge import KLSearchParam, KLUpdateParam, KLCreateParam, KLRead, KlDetails
from common.exception import errors
from utils.serializers import select_as_dict


class CRUDKl:
    def __init__(self, model):
        self.model = model

    async def search(self, db: AsyncSession, param: KLSearchParam) -> Sequence[Knowledge]:
        where_list = []
        if param.kl_content:
            where_list.append(self.model.kl_content.like(f'%{param.kl_content}%'))
        if param.kl_title:
            where_list.append(self.model.kl_title.like(f'%{param.kl_title}%'))
        if param.kl_label:
            where_list.append(self.model.kl_label.any(Label.label_id.in_(param.kl_label)))
        if param.kl_state:
            where_list.append(self.model.kl_state == param.kl_state)
        stat = select(self.model).filter(
            and_(*where_list)
        ).options(selectinload(self.model.kl_label)).limit(param.size).offset(param.page * param.size)
        result = await db.execute(stat)
        return result.scalars().all()

    async def create(self, db: AsyncSession, kl: KLCreateParam) -> KLRead:
        db_kl = self.model(**kl.dict())
        db.add(db_kl)
        await db.flush()
        await db.refresh(db_kl)
        data = KLRead.from_orm(await db.get(Knowledge, db_kl.kl_id))
        await db.commit()
        return data

    async def delete(self, db: AsyncSession, kl_id: int):
        stat = select(self.model).filter(self.model.kl_id == kl_id)
        data = await db.scalars(stat)
        db_kl = data.first()
        if not db_kl:
            raise errors.NotFoundError(msg='删除一个不存在的知识')
        await db.delete(db_kl)
        await db.commit()

    async def update(self, db: AsyncSession, kl: KLUpdateParam):
        stat = select(self.model).filter(self.model.kl_id == kl.kl_id)
        data = await db.scalars(stat)
        kl1 = data.first()
        if not kl1:
            raise errors.NotFoundError(msg='知识不存在')
        if kl.kl_title:
            kl1.kl_title = kl.kl_title
        if kl.kl_content:
            kl1.kl_content = kl.kl_content
        if kl.kl_like_change:
            kl1.kl_like += kl.kl_like_change
        if kl.kl_dislike_change:
            kl1.kl_dislike += kl.kl_dislike_change
        if kl.kl_hot_change:
            kl1.kl_hot += kl.kl_hot_change
        if kl.kl_state_change:
            kl1.kl_state = kl.kl_state_change

        await db.flush()
        await db.refresh(kl1)
        data1 = KLRead.from_orm(await db.get(Knowledge, kl1.kl_id))
        await db.commit()
        return data1

    async def getKLDetails(self, db: AsyncSession, kl_id: int) -> KlDetails:
        stat = (select(self.model)
                .options(joinedload(self.model.user),
                         joinedload(self.model.kl_label).joinedload(KlLabel.label),
                         joinedload(self.model.annex),
                         joinedload(self.model.comment)
                         )
                .where(self.model.kl_id == kl_id)
                )
        row = (await db.scalars(stat)).first()
        if not row:
            raise errors.NotFoundError(msg='知识不存在')

        # data = KlDetails(** await select_as_dict(row))
        data = KlDetails.from_orm(row)
        return data




kl_dao = CRUDKl(Knowledge)
