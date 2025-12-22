from sqlalchemy import select
from sqlalchemy.orm import joinedload

from ..dto.create_post_dto import CreatePostDto
from ....database import async_session
from ....models.models import Account, Author, Post, AuthorType
from ....schemas.account_schema import ShortAccountSchema
from ....schemas.post_schema import ShortPostAccountSchema
from ....shared.errors.exceptions.not_found_exception import NotFoundException


async def create_account_post(create_post_data: CreatePostDto):
    async with async_session() as session:
        account_result = await session.execute(select(Account).options(
            joinedload(Account.posts),
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
            author_type=AuthorType.account,
            author_id=author.id,
        )
        session.add(new_post)
        await session.commit()

        serialized_post = ShortPostAccountSchema.model_validate(new_post, from_attributes=True)
        validated_account = ShortAccountSchema.model_validate(new_post.author.account, from_attributes=True)

        serialized_post.author = validated_account.model_dump()

        return serialized_post
