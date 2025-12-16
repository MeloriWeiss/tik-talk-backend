from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.models import Community, Comment, Author
from models.base import Base
from models.models import Account, Post, AuthorType

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@tik-talk-main_db-1:5432/maindb"

engine = create_engine(DATABASE_URL, echo=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def seed():
    session = Session()

    session.query(Post).delete()
    session.query(Community).delete()
    session.query(Account).delete()
    session.query(Author).delete()
    session.query(Comment).delete()
    session.commit()

    # pass 12345
    account1 = Account(
        username="Alice",
        hashed_password="1d71706deabdbd77fc20859f828204f2:58f93139bfd8fb17b5d57808601bd7eec2ce609c4a60673a64611bc08e96cee8"
    )
    account2 = Account(
        username="Max",
        hashed_password="1d71706deabdbd77fc20859f828204f2:58f93139bfd8fb17b5d57808601bd7eec2ce609c4a60673a64611bc08e96cee8"
    )
    session.add_all([account1, account2])
    session.commit()

    account1_author = Author(
        type=AuthorType.account,
        account=account1,
    )
    account2_author = Author(
        type=AuthorType.account,
        account=account2,
    )
    session.add_all([account1_author, account2_author])
    session.commit()

    post1 = Post(
        title="Post1 title",
        content="Post1 content",
        author_type=AuthorType.account,
        author_id=account1_author.id,
    )
    post2 = Post(
        title="Post2 title",
        content="Post2 content",
        author_type=AuthorType.account,
        author_id=account2_author.id,
    )
    session.add_all([post1, post2])
    session.commit()

    community1 = Community(
        admin_id=account1.id,
        name="Angular community 1",
        description="Community 1 description",
        tags=["Angular", "Programming"],
        themes=["Coding", "Psychology"],
    )
    session.add_all([community1])
    session.commit()

    community1_author = Author(
        type=AuthorType.account,
        community=community1,
    )
    session.add_all([community1_author])
    session.commit()

    post3 = Post(
        title="Post3 title",
        content="Post3 content",
        author_type=AuthorType.community,
        author_id=community1_author.id,
    )
    session.add_all([post3])
    session.commit()

    account1.subscriptions.append(account2)
    account1.subscribers.append(account2)
    session.commit()

    session.close()


if __name__ == "__main__":
    seed()
    print("Database maindb seeded successfully.")