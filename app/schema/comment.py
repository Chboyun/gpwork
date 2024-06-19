from datetime import datetime

from pydantic import ConfigDict, Field


from app.schema.user import UserDetails
from common.schema import SchemaBase


class CommentBase(SchemaBase):
    comment_content: str
    kl_id: int
    user_id: int


class CommentCreateParam(CommentBase):
    pass


class CommentDetails(CommentBase):
    comment_id: int
    user: UserDetails
    create_time: datetime
    update_time: datetime

    model_config = ConfigDict(from_attributes=True)