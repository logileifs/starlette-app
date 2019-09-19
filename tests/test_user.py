import asyncio
from http import HTTPStatus as status

from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

import asynctest
from async_asgi_testclient import TestClient

from api import db
from api.app import app
from api.schemas.user import User
from tests.asserts import *


async def create_user():
	#await db.connect()
	u = User(name='glommi')
	await u.save()
	return u


def run_async(func):
	value = asyncio.get_event_loop().run_until_complete(func())
	return value


class MinimalExample(asynctest.TestCase):

	def test_that_true_is_true(self):
		assert_true(True)

	async def test_app(self):
		async with TestClient(app) as client:
			response = await client.get('/')
			assert_equal(response.status_code, 200)

	async def test_create_user(self):
		async with TestClient(app) as client:
			gizur = {'name': 'gizur'}
			rsp = await client.post('/users/', json=gizur)
			assert_equal(rsp.status_code, status.CREATED)
			data = rsp.json()
			assert_equal(data['name'], 'gizur')

	async def test_get_user(self):
		async with TestClient(app) as client:
			user = await create_user()
			rsp = await client.get('/user/%s' % user.id)
			assert_equal(rsp.status_code, status.OK)
			data = rsp.json()
			print('data: %s' % data)
			assert_equal(data['id'], user.id)
			#assert_equal(data['name'], user.name)

	async def test_get_all_users(self):
		async with TestClient(app) as client:
			rsp = await client.get('/users/')
			assert_equal(rsp.status_code, status.OK)
			data = rsp.json()
			assert_true('users' in data)
