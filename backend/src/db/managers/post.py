from typing import Type, List

from tortoise.contrib.pydantic import pydantic_model_creator

import src
from src.db.manager import Manager
from src.db.models import Post
from src.rest.schemas import ModPost


PostBody = pydantic_model_creator(Post, name="Post")


class PostManager(Manager, metaclass=src.Singleton):
    model = Post

    @classmethod
    async def add(cls, body: ModPost) -> PostBody:
        return await PostBody.from_tortoise_orm(
            await cls.model.create(**body.dict(exclude_unset=True, exclude={'id'}))
        )

    @classmethod
    async def all(cls) -> List[PostBody]:
        return await PostBody.from_queryset(cls.model.all())

    @classmethod
    async def get(cls, _id: int) -> PostBody:
        return await PostBody.from_queryset_single(cls.model.get(id=_id))


async def get_manager() -> Type[Manager]:
    return PostManager


__all__ = [
    'PostManager',
    'PostBody',
    'get_manager'
]
