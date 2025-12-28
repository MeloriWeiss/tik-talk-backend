from datetime import datetime

from pydantic import BaseModel

from .account_schema import ShortAccountSchema


class CommentSchema(BaseModel):
    id: int
    text: str
    author: ShortAccountSchema
    postId: int
    commentId: int
    createdAt: datetime
    updatedAt: datetime