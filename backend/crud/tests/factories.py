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
    async def create(cls, **params: Optional) -> models.User:
        return await cls.model.create(
            username='@' + fake.unique.user_name(),
            password_hash=fake.unique.password,
            active=params.get('active', True)
        )


class FakePost(AbsFakeModel):
    model = models.Post

    @classmethod
    async def create(cls, **params: Optional) -> MODEL:
        return await cls.model.create(
            title=fake.unique.name(),
            text=fake.unique.text(),
            video_link=fake.unique.uri()
        )


class FakeComment(AbsFakeModel):
    model = models.Comment

    @classmethod
    async def create(cls, **params: Optional) -> MODEL:
        return await cls.model.create(
            text=fake.unique.text()
        )


class FakeImage(AbsFakeModel):
    model = models.Image

    @classmethod
    async def create(cls, **params: Optional) -> MODEL:
        return await cls.model.create(
            main=params.get('main', False),
            image=fake.image(size=(2, 2), hue='purple', luminosity='bright', image_format='ico'),
            user=params.get('user'),
            post=params.get('post'),
            comment=params.get('comment')
        )
