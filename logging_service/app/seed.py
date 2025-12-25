from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Log
from models.base import LogsBase

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@tik-talk-logs_db-1:5432/logsdb"

engine = create_engine(DATABASE_URL, echo=True)

LogsBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def seed():
    session = Session()

    log1 = Log()
    log2 = Log()

    session.add_all([log1, log2])
    session.commit()
    session.close()


if __name__ == "__main__":
    seed()
    print("Database logsdb seeded successfully.")
