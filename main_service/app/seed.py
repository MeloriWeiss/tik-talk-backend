from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Community, Comment, Author, Chat, Message
from models.base import Base
from models.models import Account, Post, AuthorType

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@tik-talk-main_db-1:5432/maindb"

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def seed():
    session = Session()

    session.query(Message).delete()
    session.query(Chat).delete()
    session.query(Post).delete()
    session.query(Community).delete()
    session.query(Account).delete()
    session.query(Author).delete()
    session.query(Comment).delete()
    session.flush()

    # pass 12345
    account1 = Account(
        username="Alice",
        hashed_password="1d71706deabdbd77fc20859f828204f2:58f93139bfd8fb17b5d57808601bd7eec2ce609c4a60673a64611bc08e96cee8"
    )
    account2 = Account(
        username="Max",
        hashed_password="1d71706deabdbd77fc20859f828204f2:58f93139bfd8fb17b5d57808601bd7eec2ce609c4a60673a64611bc08e96cee8"
    )
    account3 = Account(
        username="Elise",
        hashed_password="1d71706deabdbd77fc20859f828204f2:58f93139bfd8fb17b5d57808601bd7eec2ce609c4a60673a64611bc08e96cee8"
    )
    session.add_all([account1, account2, account3])
    session.flush()

    account1_author = Author(
        type=AuthorType.ACCOUNT,
        account=account1,
    )
    account2_author = Author(
        type=AuthorType.ACCOUNT,
        account=account2,
    )
    account3_author = Author(
        type=AuthorType.ACCOUNT,
        account=account3,
    )
    session.add_all([account1_author, account2_author, account3_author])
    session.flush()

    post1 = Post(
        title="Post1 title",
        content="Post1 content",
        author_type=AuthorType.ACCOUNT,
        author_id=account1_author.id,
    )
    post2 = Post(
        title="Post2 title",
        content="Post2 content",
        author_type=AuthorType.ACCOUNT,
        author_id=account2_author.id,
    )
    session.add_all([post1, post2])
    session.flush()

    community1 = Community(
        admin_id=account1.id,
        name="Angular community 1",
        description="Community 1 description",
        tags=["Angular", "Programming"],
        themes=["Coding", "Psychology"],
    )
    session.add_all([community1])
    session.flush()

    community1_author = Author(
        type=AuthorType.ACCOUNT,
        community=community1,
    )
    session.add_all([community1_author])
    session.flush()

    post3 = Post(
        title="Post3 title",
        content="Post3 content",
        author_type=AuthorType.COMMUNITY,
        author_id=community1_author.id,
    )
    session.add_all([post3])
    session.flush()

    account1.subscriptions.append(account2)
    account1.subscribers.append(account2)
    session.flush()

    chat1 = Chat(
        userFirstId=account1.id,
        userSecondId=account2.id,
    )
    session.add_all([chat1])
    session.flush()

    message1 = Message(
        userFromId=account1.id,
        personalChatId=chat1.id,
        text="Seed message 1",
        chatId=chat1.id,
    )
    session.add_all([message1])
    session.flush()

    session.commit()
    session.close()


if __name__ == "__main__":
    seed()
    print("Database maindb seeded successfully.")
