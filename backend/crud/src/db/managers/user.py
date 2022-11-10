from typing import Type

from tortoise.contrib.pydantic import pydantic_model_creator

import src
from src.db.manager import Manager
from src.db.models import User
from src.rest.schemas import ModUser
from src.utils import Password


UserBody = pydantic_model_creator(User, name='User')


class UserManager(Manager, metaclass=src.Singleton):
    model = User
    response = UserBody

    @classmethod
    async def add(cls, body: ModUser) -> UserBody:
        user = (await cls.model.get_or_create(
            username=body.username,
            defaults={
                'password_hash': Password.hash(body.password_hash),
                'active': body.active
            }
        ))[0]
        return await UserBody.from_tortoise_orm(user)


async def get_manager() -> Manager:
    return UserManager()


__all__ = [
    'UserManager',
    'UserBody',
    'get_manager'
]
