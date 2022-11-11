from typing import Optional
from abc import abstractclassmethod

import faker
from tortoise.models import MODEL

from src.db import models


fake = faker.Faker()


class AbsFakeModel:
    model: MODEL

    @abstractclassmethod
    async def create(cls, **params: Optional) -> MODEL: ...


class FakeUser(AbsFakeModel):
    model = models.User

    @classmethod
    async def create(cls, active: int = True) -> models.User:
        return await cls.model.create(
            username='@' + fake.unique.name().lower().replace(' ', '_'),
            password_hash=fake.unique.password,
            active=active
        )
