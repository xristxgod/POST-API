import json
from typing import Callable

import pytest
from httpx import AsyncClient

from src.db.models import User
from src.db.managers.user import UserBody


@pytest.mark.anyio
class TestView:

    model = User
    endpoint = '/api/users'

    # @pytest.mark.parametrize()
    async def test_create_user(self, client: AsyncClient):
        data = dict(username='@test-testov', password='2412455xfasd231')

        response = await client.post(self.endpoint, data=data)

        assert response.status_code == 200
        assert response.json()['username'] == data['username']
        assert response.json()['active'] is True

    async def test_get_user(self, client: AsyncClient, fake_user: Callable):
        user = await fake_user()

        response = await client.get(self.endpoint + f'/{user.pk}')

        assert response.status_code == 200
        assert json.dumps(response.json()) == (await UserBody.from_tortoise_orm(user)).json()

    async def test_get_all_users(self, client: AsyncClient, fake_user: Callable):
        await fake_user()
        await fake_user(active=False)

        response = await client.get(self.endpoint + '/all')

        assert response.status_code == 200
        assert len(response.json()) == len(await self.model.all())
