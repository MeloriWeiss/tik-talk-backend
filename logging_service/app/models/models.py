from sqlalchemy import Column, Integer, String, Enum, Boolean, TIMESTAMP
import enum
from datetime import datetime, timezone

from .base import LogsBase


class LogType(str, enum.Enum):
    info = "info"
    error = "error"
    critical = "critical"


class Log(LogsBase):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Enum(LogType), default=LogType.info)
