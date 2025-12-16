from fastapi import Query
from pydantic import BaseModel


class CommunitiesFiltersDto(BaseModel):
    name: str | None = Query(None)
    themes: list[str] | None = Query(None)
    tags: list[str] | None = Query(None)
    page: int | None = Query(None)
    size: int | None = Query(None)