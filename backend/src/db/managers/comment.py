from typing import Type, List

from tortoise.contrib.pydantic import pydantic_model_creator

import src
from src.db.manager import Manager
from src.db.models import Comment
from src.rest.schemas import ModComment


CommentBody = pydantic_model_creator(Comment, name="Post")


class CommentManager(Manager, metaclass=src.Singleton):
    model = Comment
    body = CommentBody

    @classmethod
    async def add(cls, body: ModComment) -> CommentBody:
        return await CommentBody.from_tortoise_orm(
            await cls.model.create(**body.dict(exclude_unset=True))
        )

    @classmethod
    async def all(cls) -> List[CommentBody]:
        return await CommentBody.from_queryset(cls.model.all())

    @classmethod
    async def get(cls, _id: int) -> CommentBody:
        return await CommentBody.from_queryset_single(cls.model.get(id=_id))

    @classmethod
    async def update(cls, _id: int, body: ModPost) -> CommentBody:
        return await CommentBody.from_tortoise_orm(
            await super(PostManager, cls).update(_id=_id, body=body)
        )


