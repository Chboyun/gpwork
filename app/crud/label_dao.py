from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.label import LabelCreateParam, LabelDetails, GetLabelLists, LabelUpdateParam, LabelRead
from sqlalchemy.sql import and_, asc, or_, select
from app.model.all_model import Label, Knowledge, KlLabel
from common.exception import errors
from database.db_mysql import async_db_session
import asyncio


class CRUDLabel:
    def __init__(self, model):
        self.model = model

    # 创建标签
    async def create(self, db: AsyncSession, label: LabelCreateParam) -> LabelRead:
        db_label = self.model(**label.dict())
        db.add(db_label)
        await db.flush()
        await db.refresh(db_label)
        data = LabelRead.from_orm(await db.get(Label, db_label.label_id))
        await db.commit()

        return data

    async def delete(self, db: AsyncSession, label_id: int) -> None:
        stat = select(self.model).filter(self.model.label_id == label_id)
        data = await db.scalars(stat)
        db_label = data.first()
        if not db_label:
            raise errors.NotFoundError(msg='删除一个不存在的标签')

        await db.delete(db_label)
        await db.commit()

    async def update(self, db: AsyncSession, param_label: LabelUpdateParam) -> LabelRead:
        stat = select(self.model).filter(self.model.label_id == param_label.label_id)
        data = await db.scalars(stat)
        label1 = data.first()
        if not label1:
            raise errors.NotFoundError(msg='标签不存在')
        if param_label.label_name:
            label1.label_name = param_label.label_name
        if param_label.description:
            label1.description = param_label.description
        await db.flush()
        await db.refresh(label1)
        data = LabelRead.from_orm(await db.get(Label, label1.label_id))
        await db.commit()
        return data

    # 获取标签列表
    async def get_all(self, db: AsyncSession) -> Sequence[Label]:
        result = await db.execute(select(self.model))
        return result.scalars().all()

    async def add_label_to_kl(self, db: AsyncSession, kl_id: int, label_id: int) -> None:
        stat = select(Label).filter(Label.label_id == label_id)
        data = await db.scalars(stat)
        label = data.first()
        if not label:
            raise errors.NotFoundError(msg='标签不存在')
        stat = select(Knowledge).filter(Knowledge.kl_id == kl_id)
        data = await db.scalars(stat)
        kl = data.first()
        if not kl:
            raise errors.NotFoundError(msg='知识不存在')

        data = KlLabel(kl_id=kl_id, label_id=label_id)
        db.add(data)
        await db.flush()
        await db.refresh(data)
        await db.commit()

    async def delete_label_from_kl(self, db: AsyncSession, kl_id: int, label_id: int) -> None:
        stat = select(KlLabel).filter(KlLabel.kl_id == kl_id).filter(KlLabel.label_id == label_id)
        data = await db.scalars(stat)
        kl_label = data.first()
        if not kl_label:
            raise errors.NotFoundError(msg='删除一个不存在的标签')
        await db.delete(kl_label)
        await db.commit()


label_dao = CRUDLabel(Label)
