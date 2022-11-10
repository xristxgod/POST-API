from typing import NoReturn, Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

import src


class MongoCore(metaclass=src.Singleton):
    __slots__ = ('_client', '_db')

    def __init__(self):
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None

    async def connect(self, path: str, **settings) -> NoReturn:
        self._client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10, **settings)
        self._db = self._client.main_db

    async def close(self) -> NoReturn:
        if self._client is not None:
            self._client.close()

    @property
    def client(self) -> AsyncIOMotorClient:
        return self._client

    @property
    def db(self) -> AsyncIOMotorDatabase:
        return self._db


__all__ = [
    'MongoCore'
]
