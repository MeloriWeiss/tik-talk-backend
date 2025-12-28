from fastapi import APIRouter, Depends
from sqlalchemy import select, cast, String
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from starlette.responses import JSONResponse

from .dto.get_http_logs_dto import GetHttpLogsDTO
from ...database import get_async_session
from ...models.models import HttpLog
from ...schemas.http_log_schema import HttpLogSchema
from ...utils.check_auth import check_auth
from ...utils.serialize_datetime import serialize_datetime

http_logs_router = APIRouter(prefix="/http", tags=["HttpLog"])


@http_logs_router.get("/")
async def get_http_logs(request: Request, filters: GetHttpLogsDTO = Depends(), session: AsyncSession = Depends(get_async_session)):
    await check_auth(request)

    logs_query = select(HttpLog)

    if filters.level:
        logs_query = logs_query.filter(cast(HttpLog.level, String).ilike(f"%{filters.level}%"))

    if filters.service:
        logs_query = logs_query.filter(HttpLog.service.ilike(f"%{filters.service}%"))

    if filters.start_time:
        logs_query = logs_query.filter(HttpLog.createdAt >= filters.start_time)

    if filters.end_time:
        logs_query = logs_query.filter(HttpLog.createdAt <= filters.end_time)

    logs_query = logs_query.offset((filters.page - 1) * filters.size).limit(filters.size)

    logs_result = await session.execute(logs_query)
    logs = logs_result.scalars().all()

    serialized_logs = [serialize_datetime(HttpLogSchema.model_validate(log).model_dump()) for log in
                       logs]

    return JSONResponse({"logs": serialized_logs})