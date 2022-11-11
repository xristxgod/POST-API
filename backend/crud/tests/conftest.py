from typing import Callable

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

import main


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=main.app, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await Tortoise.init(
        db_url='sqlite://test-db.sqlite3',
        modules={'models': ['src.db.models']},
        _create_db=True
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope="session")
async def fake_user() -> Callable:
    from .factories import FakeUser
    return FakeUser.create
