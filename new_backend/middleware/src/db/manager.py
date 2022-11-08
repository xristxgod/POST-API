from typing import NoReturn, List

from pydantic import BaseModel

from src.db.mongo import core
from src.db.base import OID


class Manager:

    model: BaseModel
    collection_name: str

    __slots__ = (
        'core', 'collection'
    )

    def __init__(self):
        self.core = core
        self.collection = getattr(self.core.db, self.collection_name)

    async def add(self, body: BaseModel) -> BaseModel: ...

    async def all(self) -> List[BaseModel]: ...

    async def get(self, _id: OID) -> BaseModel: ...

    async def update(self, _id: OID, body: BaseModel) -> BaseModel: ...

    async def delete(self, _id: OID) -> NoReturn: ...


__all__ = [
    "Manager"
]