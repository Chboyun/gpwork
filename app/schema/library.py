from datetime import datetime

from pydantic import ConfigDict, Field

from app.schema.knowledge import KLRead
from common.schema import SchemaBase

from datetime import datetime

from pydantic import ConfigDict, Field

from common.schema import SchemaBase


class LibrarySchemaBase(SchemaBase):
    library_name: str = Field(..., title='标签名称')
    description: str = Field(..., title='标签描述')


class LibraryCreateParam(LibrarySchemaBase):
    pass


class LibrarySearchParam(LibrarySchemaBase):
    pass


class LibraryRead(LibrarySchemaBase):
    model_config = ConfigDict(from_attributes=True)
    library_id: int
    create_time: datetime
    update_time: datetime


class LibraryUpdateParam(LibrarySchemaBase):
    library_id: int


class LibraryDetails(LibrarySchemaBase):
    model_config = ConfigDict(from_attributes=True)
    library_id: int
    create_time: datetime
    update_time: datetime


class KlLibraryDetails(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    kl_library_id: int
    library_id: int
    kl: KLRead


class LibraryKlList(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    kl_library: list[KlLibraryDetails]
