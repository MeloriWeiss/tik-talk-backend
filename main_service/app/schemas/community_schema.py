from pydantic import BaseModel

from ..schemas.account_schema import ShortAccountSchema


class PostCommunitySchemaAuthorless(BaseModel):
    id: int
    content: str

    class Config:
        from_attributes = True


class CommunityShema(BaseModel):
    id: int
    name: str
    admin: ShortAccountSchema
    posts: list[PostCommunitySchemaAuthorless]

    class Config:
        from_attributes = True


class ShortCommunitySchema(BaseModel):
    id: int
    name: str
    admin: ShortAccountSchema

    class Config:
        from_attributes = True


class ShortCommunitySchemaAdminless(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True