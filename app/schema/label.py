from datetime import datetime

from pydantic import ConfigDict, Field

from common.schema import SchemaBase


class LabelSchemaBase(SchemaBase):
    label_name: str = Field(..., title='标签名称')
    description: str = Field(..., title='标签描述')


class LabelCreateParam(LabelSchemaBase):
    pass


class LabelSearchParam(LabelSchemaBase):
    pass


class LabelRead(LabelSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    label_id: int
    create_time: datetime | None = None
    update_time: datetime | None = None


class LabelUpdateParam(LabelSchemaBase):
    label_id: int


class LabelDetails(LabelSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    label_id: int
    create_time: datetime
    update_time: datetime


class KlLabelDetails(SchemaBase):
    model_config = ConfigDict(from_attributes=True)
    kl_label_id: int
    label_id: int
    label: LabelDetails


# 定义 获取标签列表 的返回值
class GetLabelLists(LabelSchemaBase):
    model_config = ConfigDict(from_attributes=True)
    label_list: list[LabelDetails]
