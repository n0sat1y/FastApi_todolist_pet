from app.main import app
from httpx import AsyncClient, ASGITransport
import pytest


@pytest.mark.asyncio
async def test_get_books(client):
	response = await client.get('/tasks')
	data = response.json()
	assert response.status_code == 200
	assert len(data) > 0

@pytest.mark.asyncio
async def test_create_user(client):
	response = await client.post('/users/register', json={
		'email': 'test@user.com',
		'password': 'user'
	})
	print(response.json())