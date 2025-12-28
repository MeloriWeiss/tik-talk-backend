import enum
from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey, TIMESTAMP, Table
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship

from .base import Base


class AuthorType(str, enum.Enum):
    ACCOUNT = "account"
    COMMUNITY = "community"


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, index=True)
    type = Column(Enum(AuthorType), nullable=False)

    account = relationship("Account", uselist=False, back_populates="author", cascade="all, delete")
    community = relationship("Community", uselist=False, back_populates="author", cascade="all, delete")


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False, default="")
    content = Column(String(1000), nullable=False)

    author_type = Column(Enum(AuthorType), nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author")

    images = Column(ARRAY(String), default=[])
    likes = Column(Integer, default=0)
    likesUsers = Column(ARRAY(String), default=[])

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    comments = relationship("Comment", back_populates="post")


account_to_account_subscriptions = Table(
    'account_to_account_subscriptions',
    Base.metadata,
    Column('subscriber_id', Integer, ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True),
    Column('subscribed_to_id', Integer, ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True),
)

account_to_community_subscriptions = Table(
    'account_to_community_subscriptions',
    Base.metadata,
    Column('account_id', Integer, ForeignKey('accounts.id', ondelete='CASCADE'), primary_key=True),
    Column('community_id', Integer, ForeignKey('communities.id', ondelete='CASCADE'), primary_key=True),
)


class Roles(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    avatar_url = Column(String(200))
    subscribersAmount = Column(Integer, nullable=False, default=0)
    firstName = Column(String(50))
    lastName = Column(String(50))
    isActive = Column(Boolean, default=True)
    stack = Column(ARRAY(String(50)), default=[])
    city = Column(String(50))
    description = Column(String(300))
    hashed_password = Column(String, nullable=False)
    roles = Column(ARRAY(Enum(Roles)), default=[Roles.USER])

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="account")

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    comments = relationship("Comment", back_populates="author")

    subscriptions = relationship(
        'Account',
        secondary=account_to_account_subscriptions,
        primaryjoin=id == account_to_account_subscriptions.c.subscriber_id,
        secondaryjoin=id == account_to_account_subscriptions.c.subscribed_to_id,
        back_populates='subscribers'
    )

    subscribers = relationship(
        'Account',
        secondary=account_to_account_subscriptions,
        primaryjoin=id == account_to_account_subscriptions.c.subscribed_to_id,
        secondaryjoin=id == account_to_account_subscriptions.c.subscriber_id,
        back_populates='subscriptions'
    )

    subscribed_communities = relationship(
        'Community',
        secondary=account_to_community_subscriptions,
        back_populates='subscribers'
    )

    posts = relationship(
        'Post',
        primaryjoin='and_(Post.author_id == Account.author_id, Post.author_type == "account")',
        foreign_keys=[Post.author_id],
        viewonly=True
    )


class Community(Base):
    __tablename__ = 'communities'

    id = Column(Integer, primary_key=True, index=True)
    admin_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    admin = relationship('Account')

    name = Column(String, nullable=False)
    bannerUrl = Column(String)
    avatarUrl = Column(String)
    description = Column(String)
    subscribersAmount = Column(Integer, default=0)
    isJoined = Column(Boolean, default=False)

    author_id = Column(Integer, ForeignKey('authors.id'))
    author = relationship("Author", back_populates="community")

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    themes = Column(ARRAY(String(30)))
    tags = Column(ARRAY(String(30)))

    subscribers = relationship(
        'Account',
        secondary=account_to_community_subscriptions,
        back_populates='subscribed_communities'
    )

    posts = relationship(
        'Post',
        primaryjoin="and_(Post.author_id==Community.author_id, Post.author_type=='community')",
        foreign_keys=[Post.author_id],
        viewonly=True
    )


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    commentId = Column(Integer)

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    author_id = Column(Integer, ForeignKey('accounts.id'))
    author = relationship("Account", back_populates="comments")

    postId = Column(Integer, ForeignKey('posts.id'))
    post = relationship("Post", back_populates="comments")


class Chat(Base):
    __tablename__ = 'chats'

    id = Column(Integer, primary_key=True, index=True)

    messages = relationship("Message", back_populates="chat")

    userFirstId = Column(Integer, ForeignKey('accounts.id'))
    userFirst = relationship("Account", foreign_keys="Chat.userFirstId")

    userSecondId = Column(Integer, ForeignKey('accounts.id'))
    userSecond = relationship("Account", foreign_keys="Chat.userSecondId")

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    userFromId = Column(Integer, nullable=False)
    personalChatId = Column(Integer, nullable=False)
    text = Column(String, nullable=False)
    isRead = Column(Boolean, default=False)

    createdAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))
    updatedAt = Column(TIMESTAMP(timezone=True), default=datetime.now(timezone.utc))

    chatId = Column(Integer, ForeignKey('chats.id'))
    chat = relationship("Chat", back_populates="messages")