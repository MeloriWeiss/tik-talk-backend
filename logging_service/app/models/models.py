from datetime import datetime, timezone

from sqlalchemy import Column, Integer, Enum, String, Float, TIMESTAMP
import enum

from .base import LogsBase


class LogLevel(str, enum.Enum):
    INFO = "info"
    ERROR = "error"
    CRITICAL = "critical"


class HttpLog(LogsBase):
    __tablename__ = "http_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Enum(LogLevel), default=LogLevel.INFO)
    timestamp = Column(String)
    service = Column(String)
    request_id = Column(String)
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    duration_ms = Column(Float)
    client_ip = Column(String)
    message = Column(String)

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
