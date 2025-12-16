from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.base import ChatsBase

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@tik-talk-main_db-1:5432/maindb"

engine = create_engine(DATABASE_URL, echo=True)

ChatsBase.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


# def seed():
#     session = Session()
#
#     # Создайте начальные данные
#     account1 = Account(
#         username='Alice',
#         hashed_password='12345'
#     )
#     session.add_all([account1])
#     session.commit()
#
#     post1 = Post(
#         title='Post1 title',
#         content='Post1 content',
#         author_id=account1.id,
#         author_type=AuthorType.account,
#     )
#
#
#     session.add_all([post1])
#     session.commit()
#     session.close()
#
#
# if __name__ == "__main__":
#     seed()
#     print("Database maindb seeded successfully.")