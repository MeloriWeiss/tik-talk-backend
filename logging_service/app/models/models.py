from sqlalchemy import Column, Integer, Enum, String, Float
import enum

from .base import LogsBase


class LogType(str, enum.Enum):
    info = "info"
    error = "error"
    critical = "critical"


class HttpLog(LogsBase):
    __tablename__ = "http_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Enum(LogType), default=LogType.info)
    timestamp = Column(String)
    service = Column(String)
    request_id = Column(String)
    method = Column(String)
    path = Column(String)
    status_code = Column(Integer)
    duration_ms = Column(Float)
    client_ip = Column(String)
    message = Column(String)
