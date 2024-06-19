from app.crud.kl_dao import kl_dao
from app.model.all_model import Knowledge
from app.schema.knowledge import KLSearchParam, KLCreateParam, KLRead, KLUpdateContentParam, KLUpdateParam, KlDetails
from database.db_mysql import async_db_session
from app.crud.label_dao import label_dao
from utils.serializers import select_list_serialize
from app.crud.collect_dao import collect_dao, CollectParam, CollectList


class CollectService:

    @staticmethod
    async def add_collect(obj: CollectParam) -> KLRead:
        async with async_db_session.begin() as db:
            return await collect_dao.add_collect(db, obj)

    @staticmethod
    async def remove_collect_by_collect_id(collect_id: int, user_id: int):
        async with async_db_session.begin() as db:
            return await collect_dao.remove_collect_by_collect_id(db, collect_id, user_id)

    @staticmethod
    async def remove_collect_by_kl_id(kl_id: int, user_id: int):
        async with async_db_session.begin() as db:
            return await collect_dao.remove_collect_by_kl_id(db, kl_id, user_id)

    @staticmethod
    async def get_collect_list(user_id: int) -> CollectList:
        async with async_db_session() as db:
            return await collect_dao.get_collect_list(db, user_id)
