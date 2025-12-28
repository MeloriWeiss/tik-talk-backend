from datetime import datetime

from fastapi import Query
from pydantic import BaseModel


class GetHttpLogsDTO(BaseModel):
    level: str | None = Query(None)
    service: str | None = Query(None)
    start_time: datetime | None = Query(None)
    end_time: datetime | None = Query(None)
    page: int | None = Query(1)
    size: int | None = Query(10)