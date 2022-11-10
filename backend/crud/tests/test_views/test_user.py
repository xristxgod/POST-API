import pytest
from httpx import AsyncClient

from src.db.models import User
import main

# @pytest.mark.asyncio
# class TestView:
#
#     model = User
#     endpoint = '/api/users'
#
#     async def test_get_users(self, client: AsyncClient):
#         result = await client.get(
#             self.endpoint + '/all'
#         )
#         assert await result.json() == []


@pytest.mark.anyio
async def test_client():
    async with AsyncClient(app=main.app, base_url="http://test") as client:
        res = await client.get('/')

    assert res.statuse_code == 200
    assert res.statuse_code != 200