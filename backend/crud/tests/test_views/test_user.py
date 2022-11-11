import pytest
from httpx import AsyncClient

from src.db.models import User


@pytest.mark.anyio
class TestView:

    model = User
    endpoint = '/api/users'

    async def test_get_users(self, client: AsyncClient):
        user = await User.create(

        )