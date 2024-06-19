from datetime import datetime

from pydantic import ConfigDict, Field

from common.enums import MethodType
from common.schema import SchemaBase


class UserSchemaBase(SchemaBase):
    username: str
    password: str


class UserCreateParam(UserSchemaBase):
    pass


class UserUpdateParam(UserSchemaBase):
    user_id: int
    pass


class UserDetails(SchemaBase):
    user_id: int
    username: str
    create_time: datetime | None = None
    update_time: datetime | None = None

    model_config = ConfigDict(from_attributes=True)


class UserVerifyParam(SchemaBase):
    username: str
    user_id: int
    password: str
    create_time: datetime
    update_time: datetime

    model_config = ConfigDict(from_attributes=True)
