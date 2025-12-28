from fastapi import Query
from pydantic import BaseModel


class CommunitiesFiltersDTO(BaseModel):
    name: str | None = Query(None)
    themes: list[str] | None = Query(None)
    tags: list[str] | None = Query(None)
    page: int | None = Query(1)
    size: int | None = Query(10)