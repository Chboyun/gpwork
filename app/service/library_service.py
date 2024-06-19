from app.model.all_model import Label
from app.schema.label import LabelCreateParam, LabelUpdateParam, LabelRead
from database.db_mysql import async_db_session
from app.crud.library_dao import library_dao
from utils.serializers import select_list_serialize
from app.schema.library import LibraryCreateParam, LibraryUpdateParam, LibraryRead, LibraryDetails


class LibraryService:
    @staticmethod
    async def create(obj: LibraryCreateParam) -> LibraryRead:
        async with async_db_session.begin() as db:
            return await library_dao.create(db, obj)

    @staticmethod
    async def delete(library_id: int):
        async with async_db_session.begin() as db:
            return await library_dao.delete(db, library_id)

    @staticmethod
    async def update(obj: LibraryUpdateParam):
        async with async_db_session.begin() as db:
            return await library_dao.update(db, obj)

    @staticmethod
    async def get_all() -> list[LibraryRead]:
        async with async_db_session() as db:
            return await library_dao.get_all(db)

    @staticmethod
    async def get_kl_in_library(library_id: int) -> LibraryDetails:
        async with async_db_session() as db:
            return await library_dao.get_kl_in_library(db, library_id)


    @staticmethod
    async def add_kl_to_library(library_id: int, kl_id: int):
        async with async_db_session.begin() as db:
            return await library_dao.add_kl_to_library(db, library_id, kl_id)

    @staticmethod
    async def remove_kl_from_library(library_id: int, kl_id: int):
        async with async_db_session.begin() as db:
            return await library_dao.delete_kl_from_library(db, library_id, kl_id)



