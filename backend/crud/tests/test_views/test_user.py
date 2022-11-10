import logging

import pytest
from httpx import AsyncClient

from src.db.models import User


# @pytest.mark.anyio
# class TestUserView:
#
#     endpoint = '/api/users'
#
#     async def test_get_users(self, client: AsyncClient):
#         name, age = ["sam", 99]
#         assert await User.filter(username=name).count() == 0

@pytest.mark.asyncio
async def test_get_users(client: AsyncClient):
    # u1 = await User.all().first()
    # users = await User.all()
    print('s')