from datetime import datetime, timezone, timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Token
from models.base import AuthBase

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@tik-talk-auth_db-1:5432/authdb"

engine = create_engine(DATABASE_URL, echo=True)

AuthBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def seed():
    session = Session()

    session.query(Token).delete()

    token1 = Token(
        account_id=1,
        hashed_token="sdfsdfsdf",
        token_type="refresh",
        expires_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc)
    )
    token2 = Token(
        account_id=1,
        hashed_token="sdfsdfsdffgfdg",
        token_type="access",
        expires_at=datetime.now(timezone.utc),
        created_at=datetime.now(timezone.utc)
    )

    session.add_all([token1, token2])
    session.commit()
    session.close()


if __name__ == "__main__":
    seed()
    print("Database authdb seeded successfully.")