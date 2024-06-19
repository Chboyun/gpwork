from datetime import datetime
from pydantic import ConfigDict, Field

from app.schema.annex import AnnexDetails
from app.schema.comment import CommentDetails
from common.schema import SchemaBase
from app.schema.user import UserDetails
from app.schema.label import LabelDetails, KlLabelDetails


class KLSchemaBase(SchemaBase):
    pass


class KLCreateParam(KLSchemaBase):
    user_id: int
    kl_title: str
    kl_content: str


class KLRead(KLSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    kl_id: int
    kl_title: str
    kl_content: str
    kl_like: int
    kl_dislike: int
    kl_hot: int
    kl_state: int
    user_id: int
    create_time: datetime
    update_time: datetime


class KLUpdateParam(KLSchemaBase):
    kl_id: int
    kl_title: str | None = None
    kl_content: str | None = None
    kl_like_change: int | None = None
    kl_dislike_change: int | None = None
    kl_hot_change: int | None = None
    kl_state_change: int | None = None


class KLUpdateContentParam(KLSchemaBase):
    kl_id: int
    kl_title: str | None = None
    kl_content: str | None = None


class KLSearchParam(KLSchemaBase):
    kl_title: str | None = None
    kl_content: str | None = None
    kl_state: int | None = None
    kl_label: list[int] = Field([], title='标签列表', description='查询同时包含这些标签的知识')
    page: int = Field(0, title='页码', description='页码从0开始')
    size: int = Field(10, title='每页数量', description='每页数量')


class KlDetails(KLSchemaBase):
    kl_id: int
    kl_title: str
    kl_content: str
    kl_like: int
    kl_dislike: int
    kl_hot: int
    kl_state: int
    create_time: datetime
    update_time: datetime
    user: UserDetails
    kl_label: list[KlLabelDetails]
    annex: list[AnnexDetails]
    comment: list[CommentDetails]

    model_config = ConfigDict(from_attributes=True)
