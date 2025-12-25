from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import HttpLog
from models.base import LogsBase

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@tik-talk-logs_db-1:5432/logsdb"

engine = create_engine(DATABASE_URL, echo=True)

LogsBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def seed():
    session = Session()

    http_log1 = HttpLog(
        timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        level="info",
        service="main_service",
        request_id="dsfjskdgfjfgfdgfdggwrtgv",
        method="POST",
        path="/register",
        status_code=200,
        duration_ms=211,
        client_ip="192.168.127.12",
        message="Seed log 1",
    )
    http_log2 = HttpLog(
        timestamp=datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
        level="error",
        service="main_service",
        request_id="dsfjskdgfjfgfdgfdggwrtgv",
        method="POST",
        path="/accounts",
        status_code=401,
        duration_ms=128,
        client_ip="192.168.127.12",
        message="Seed log 2",
    )

    session.add_all([http_log1, http_log2])
    session.commit()
    session.close()


if __name__ == "__main__":
    seed()
    print("Database logsdb seeded successfully.")
