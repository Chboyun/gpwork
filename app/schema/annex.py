from datetime import datetime

from pydantic import ConfigDict, Field

from common.schema import SchemaBase


class AnnexBase(SchemaBase):
    annex_name: str
    annex_url: str


class AnnexCreateParam(AnnexBase):
    pass


class AnnexDetails(AnnexBase):
    annex_id: int
    create_time: datetime
    update_time: datetime

    model_config = ConfigDict(from_attributes=True)

