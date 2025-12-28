from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..dto.create_post_dto import CreatePostDTO
from ....database import async_session
from ....models.models import Account, Author, Post, AuthorType
from ....schemas.author_schema import ShortAuthorAccountSchema
from ....schemas.post_schema import PostSchema
from ....shared.errors.exceptions.not_found_exception import NotFoundException
from ....utils.serialize_datetime import serialize_datetime


async def create_account_post(create_post_data: CreatePostDTO):
    async with async_session() as session:
        account_result = await session.execute(select(Account).options(
            joinedload(Account.author).joinedload(Author.account)
        ).where(Account.id == create_post_data.authorId))
        account = account_result.unique().scalar_one_or_none()

        if not account:
            raise NotFoundException(detail="Account not found")

        author = account.author

        if not author:
            raise NotFoundException(detail="Author not found")

        new_post = Post(
            title=create_post_data.title,
            content=create_post_data.content,
            author_type=AuthorType.ACCOUNT,
            author_id=author.id,
        )
        session.add(new_post)
        await session.commit()

        result = await session.execute(select(Post).options(
            joinedload(Post.comments),
            joinedload(Post.author).joinedload(Author.account)
        ).where(Post.id == new_post.id))
        post = result.unique().scalar_one_or_none()

        if not post:
            raise NotFoundException("Post not found")

        serialized_post = PostSchema[ShortAuthorAccountSchema].model_validate(post)
        serialized_post.author = serialized_post.author.account.model_dump()

        return serialize_datetime(serialized_post.model_dump())
