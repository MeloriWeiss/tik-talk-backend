from pydantic import BaseModel


class CommunityCreateDTO(BaseModel):
    name: str
    themes: list[str]
    tags: list[str]
    description: str | None = None