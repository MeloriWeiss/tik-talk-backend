from datetime import datetime
from typing import Generic, TypeVar

from pydantic import BaseModel

from .comment_schema import CommentSchema

AuthorT = TypeVar('AuthorT')


class PostSchema(BaseModel, Generic[AuthorT]):
    id: int
    content: str
    author: AuthorT
    title: str
    images: list[str]
    createdAt: datetime
    updatedAt: datetime
    likes: int
    likesUsers: list[str]
    comments: list[CommentSchema]

    class Config:
        from_attributes = True


class PostSchemaAuthorAdminless(BaseModel, Generic[AuthorT]):
    id: int
    content: str
    author: AuthorT
    title: str
    images: list[str]
    createdAt: datetime
    updatedAt: datetime
    likes: int
    likesUsers: list[str]
    comments: list[CommentSchema]

    class Config:
        from_attributes = True


class PostSchemaAuthorless(BaseModel):
    id: int
    content: str
    title: str
    images: list[str]
    createdAt: datetime
    updatedAt: datetime
    likes: int
    likesUsers: list[str]
    comments: list[CommentSchema]

    class Config:
        from_attributes = True
