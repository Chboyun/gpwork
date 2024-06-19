from app.model.all_model import Label
from app.schema.label import LabelCreateParam, LabelUpdateParam, LabelRead
from database.db_mysql import async_db_session
from app.crud.label_dao import label_dao
from utils.serializers import select_list_serialize
from app.schema.label import GetLabelLists


class LabelService:
    @staticmethod
    async def get_all() -> list[Label]:
        async with async_db_session() as db:
            label_list1 = await select_list_serialize(await label_dao.get_all(db))
            return label_list1

    @staticmethod
    async def create(obj: LabelCreateParam) -> LabelRead:
        async with async_db_session.begin() as db:
            return await label_dao.create(db, obj)

    @staticmethod
    async def update(obj: LabelUpdateParam):
        async with async_db_session.begin() as db:
            return await label_dao.update(db, obj)


    @staticmethod
    async def delete(obj: int):
        async with async_db_session.begin() as db:
            await label_dao.delete(db, obj)


    @staticmethod
    async def add_label_to_kl(label_id: int, kl_id: int):
        async with async_db_session.begin() as db:
            return await label_dao.add_label_to_kl(db, label_id, kl_id)


    @staticmethod
    async def remove_label_from_kl(label_id: int, kl_id: int):
        async with async_db_session.begin() as db:
            return await label_dao.delete_label_from_kl(db, label_id, kl_id)