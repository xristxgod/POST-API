import logging

import pytest
from httpx import AsyncClient
from tortoise import Tortoise

import main
from src.settings import get_settings


SETTINGS = get_settings()


@pytest.fixture(scope="session")
async def client():
    async with AsyncClient(app=main.app, base_url="http://test") as client:
        print("Client is ready")
        yield client


@pytest.fixture(scope="session", autouse=True)
async def initialize_tests():
    await Tortoise.init(
        db_url=SETTINGS.db_pat,
        modules={'models': ['src.db.models']},
        _create_db=True
    )
    await Tortoise.generate_schemas()
    yield
    await Tortoise._drop_databases()
