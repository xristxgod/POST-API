from typing import Type, List

from tortoise.contrib.pydantic import pydantic_model_creator

import src
from src.db.manager import Manager
from src.db.models import User
from src.rest.schemas import ModUser
from src.utils import Password


UserBody = pydantic_model_creator(User, name='User')


class UserManager(Manager, metaclass=src.Singleton):
    model = User

    @classmethod
    async def add(cls, body: ModUser) -> UserBody:
        user = await cls.model.get_or_create(
            username=body.username,
            defaults={
                'password_hash': Password.hash(body.password_hash),
                'active': body.active
            }
        )
        return await UserBody.from_tortoise_orm(user[0])

    @classmethod
    async def all(cls) -> List[UserBody]:
        return await UserBody.from_queryset(cls.model.all())

    @classmethod
    async def get(cls, _id: int) -> UserBody:
        return await UserBody.from_queryset_single(cls.model.get(id=_id))

    @classmethod
    async def update(cls, _id: int, body: ModUser) -> UserBody:
        return await UserBody.from_tortoise_orm(
            await super(UserManager, cls).update(_id=_id, body=body)
        )


async def get_manager() -> Type[Manager]:
    return UserManager


__all__ = [
    'UserManager',
    'UserBody',
    'get_manager'
]
