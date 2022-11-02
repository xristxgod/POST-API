from typing import NoReturn, Optional, List
from abc import abstractclassmethod

from pydantic import BaseModel
from tortoise import models


class Manager:
    model: models.MODEL

    @abstractclassmethod
    async def add(cls, body: BaseModel) -> BaseModel: ...

    @abstractclassmethod
    async def all(cls, **kwargs: Optional) -> List[BaseModel]: ...

    @abstractclassmethod
    async def get(cls, _id: int) -> BaseModel: ...

    @classmethod
    async def update(cls, _id: int, body: BaseModel):
        item = await cls.model.get(id=_id)
        await item.update_from_dict(body.dict(exclude_unset=True, exclude_defaults=True)).save()
        return item

    @classmethod
    async def delete(cls, _id: int) -> NoReturn:
        await cls.model.filter(id=_id).delete()


__all__ = [
    "Manager"
]
