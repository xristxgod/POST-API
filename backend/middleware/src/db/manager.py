from typing import NoReturn, List

from pydantic import BaseModel
from motor import MotorCollection
import pymongo.errors as mongo_ex

from src.db.mongo import core
from src.db.base import OID


class Manager:

    model: BaseModel
    response: BaseModel
    collection_name: str

    __slots__ = (
        'core', 'collection'
    )

    def __init__(self):
        self.core = core
        self.collection: MotorCollection = getattr(self.core.db, self.collection_name)

    async def set_index(self):
        raise NotImplemented

    async def add(self, body: BaseModel) -> BaseModel:
        item = await self.collection.insert_one(
            body.dict(exclude=("id",))
        )
        return self.response(**item)

    async def all(self) -> List[BaseModel]: ...

    async def get(self, _id: OID) -> BaseModel: ...

    async def update(self, _id: OID, body: BaseModel) -> BaseModel: ...

    async def delete(self, _id: OID) -> NoReturn: ...


__all__ = [
    "Manager"
]