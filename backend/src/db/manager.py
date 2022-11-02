from typing import NoReturn, List

from pydantic import BaseModel, main
from tortoise import models


class Manager:
    model: models.MODEL
    response: main.ModelMetaclass

    @classmethod
    async def add(cls, body: BaseModel) -> main.ModelMetaclass:
        return await cls.response.from_tortoise_orm(
            await cls.model.create(**body.dict(exclude_unset=True))
        )

    @classmethod
    async def all(cls) -> List[main.ModelMetaclass]:
        return await cls.response.from_queryset(cls.model.all())

    @classmethod
    async def get(cls, _id: int) -> main.ModelMetaclass:
        return await cls.response.from_queryset_single(cls.model.get(id=_id))

    @classmethod
    async def update(cls, _id: int, body: BaseModel) -> main.ModelMetaclass:
        item = await cls.model.get(id=_id)
        await item.update_from_dict(body.dict(exclude_unset=True, exclude_defaults=True)).save()
        return cls.response.from_tortoise_orm(item)

    @classmethod
    async def delete(cls, _id: int) -> NoReturn:
        await cls.model.filter(id=_id).delete()


__all__ = [
    "Manager"
]
