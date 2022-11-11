import faker

from src.db import models


fake = faker.Faker()


class FakeUser:
    model = models.User

    @classmethod
    async def create(cls, active: int = True):
        await cls.model.create(
            username='@' + fake.unique.name().lower().replace(' ', '_'),
            password_hash=fake.unique.password,
            active=active
        )
