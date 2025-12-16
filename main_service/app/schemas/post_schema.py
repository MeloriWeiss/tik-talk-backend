from pydantic import BaseModel

from .author_schema import ShortAuthorAccountSchema, ShortAuthorCommunitySchema, ShortAuthorCommunitySchemaAdminless
from ..schemas.author_schema import AuthorAccountSchema, AuthorCommunitySchema


class PostAccountSchema(BaseModel):
    id: int
    content: str
    author: AuthorAccountSchema

    class Config:
        from_attributes = True


class ShortPostAccountSchema(BaseModel):
    id: int
    content: str
    author: ShortAuthorAccountSchema

    class Config:
        from_attributes = True


class PostCommunitySchema(BaseModel):
    id: int
    content: str
    author: AuthorCommunitySchema

    class Config:
        from_attributes = True

class ShortPostCommunitySchema(BaseModel):
    id: int
    content: str
    author: ShortAuthorCommunitySchema

    class Config:
        from_attributes = True

class ShortPostCommunitySchemaAdminless(BaseModel):
    id: int
    content: str
    author: ShortAuthorCommunitySchemaAdminless

    class Config:
        from_attributes = True