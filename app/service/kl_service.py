from app.crud.kl_dao import kl_dao
from app.model.all_model import Knowledge
from app.schema.knowledge import KLSearchParam, KLCreateParam, KLRead, KLUpdateContentParam, KLUpdateParam, KlDetails
from database.db_mysql import async_db_session
from app.crud.label_dao import label_dao
from utils.serializers import select_list_serialize


class KLService:
    @staticmethod
    async def search(param: KLSearchParam) -> list[Knowledge]:
        async with async_db_session() as db:
            kl_list = await kl_dao.search(db, param)
            return await select_list_serialize(kl_list)

    @staticmethod
    async def create(obj: KLCreateParam) -> KLRead:
        async with async_db_session.begin() as db:
            return await kl_dao.create(db, obj)

    @staticmethod
    async def change_content(obj: KLUpdateContentParam) -> KLRead:
        async with async_db_session.begin() as db:
            return await kl_dao.update(db, KLUpdateParam(**obj.dict()))

    @staticmethod
    async def like_change(kl_id: int, num: int) -> KLRead:
        async with async_db_session.begin() as db:
            return await kl_dao.update(db, KLUpdateParam(kl_id=kl_id, kl_like_change=num))

    @staticmethod
    async def dislike_change(kl_id: int, num: int) -> KLRead:
        async with async_db_session.begin() as db:
            return await kl_dao.update(db, KLUpdateParam(kl_id=kl_id, kl_dislike_change=num))

    @staticmethod
    async def state_change(kl_id: int, num: int) -> KLRead:
        async with async_db_session.begin() as db:
            return await kl_dao.update(db, KLUpdateParam(kl_id=kl_id, kl_state_change=num))


    @staticmethod
    async def getKlDetails(kl_id: int) -> KlDetails:
        async with async_db_session() as db:
            kl = await kl_dao.getKLDetails(db, kl_id)
            return kl
