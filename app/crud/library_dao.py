from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.schema.label import LabelCreateParam, LabelDetails, GetLabelLists, LabelUpdateParam, LabelRead
from sqlalchemy.sql import and_, asc, or_, select
from app.model.all_model import Label, Knowledge, KlLabel, Library, KlLibrary
from app.schema.library import LibraryUpdateParam, LibraryCreateParam, LibraryRead, LibraryKlList
from common.exception import errors
from database.db_mysql import async_db_session
import asyncio

from utils.serializers import select_list_serialize


class CRUDLibrary:
    def __init__(self, model):
        self.model = model

    async def create(self, db: AsyncSession, param: LibraryCreateParam) -> LibraryRead:
        db_library = self.model(**param.dict())
        db.add(db_library)
        await db.flush()
        await db.refresh(db_library)
        data = LibraryRead.from_orm(await db.get(Library, db_library.library_id))
        await db.commit()
        return data

    async def delete(self, db: AsyncSession, library_id: int) -> None:
        stat = select(self.model).filter(self.model.library_id == library_id)
        data = await db.scalars(stat)
        db_label = data.first()
        if not db_label:
            raise errors.NotFoundError(msg='删除一个不存在的知识库')
        await db.delete(db_label)
        await db.commit()

    async def update(self, db: AsyncSession, param: LibraryUpdateParam) -> LibraryRead:
        stat = select(self.model).filter(self.model.library_id == param.library_id)
        data = await db.scalars(stat)
        label1 = data.first()
        if not label1:
            raise errors.NotFoundError(msg='知识库不存在')
        if param.library_name:
            label1.library_name = param.library_name
        if param.description:
            label1.description = param.description
        await db.flush()
        await db.refresh(label1)
        data = LibraryRead.from_orm(await db.get(Library, label1.library_id))
        await db.commit()
        return data

    async def get_all(self, db: AsyncSession) -> list[Library]:
        result = (await db.scalars(select(self.model))).all()
        return await select_list_serialize(result)

    async def get_kl_in_library(self, db: AsyncSession, library_id: int) -> LibraryKlList:
        stat = (select(self.model)
                .options(joinedload(self.model.kl_library).joinedload(KlLibrary.kl))
                .filter(self.model.library_id == library_id))
        row = (await db.scalars(stat)).first()
        data = LibraryKlList.from_orm(row)
        return data

    async def delete_kl_from_library(self, db: AsyncSession, library_id: int, kl_id: int) -> None:
        stat = (select(KlLibrary)
                .filter(KlLibrary.library_id == library_id)
                .filter(KlLibrary.kl_id == kl_id))
        row = (await db.scalars(stat)).first()
        if not row:
            raise errors.NotFoundError(msg='不存在')
        await db.delete(row)
        await db.commit()

    async def add_kl_to_library(self, db: AsyncSession, library_id: int, kl_id: int) -> None:
        stat = (select(KlLibrary)
                .filter(KlLibrary.library_id == library_id)
                .filter(KlLibrary.kl_id == kl_id))
        row = (await db.scalars(stat)).first()
        if row:
            raise errors.NotFoundError(msg='已经存在')
        db_kl = KlLibrary(library_id=library_id, kl_id=kl_id)
        db.add(db_kl)
        await db.flush()
        await db.commit()


library_dao = CRUDLibrary(Library)
