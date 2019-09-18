import asyncio
from http import HTTPStatus as status

from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

import asynctest

from api import db
from api.app import app
from api.schemas.user import User
from tests.asserts import *


async def create_user():
	u = User(name='glommi')
	await u.save()
	return u


def run_async(func):
	value = asyncio.get_event_loop().run_until_complete(func())
	return value


class MinimalExample(asynctest.TestCase):

	def test_that_true_is_true(self):
		assert_true(True)

	def test_app(self):
		with TestClient(app) as client:
			response = client.get('/')
			assert_equal(response.status_code, 200)

	def test_create_user(self):
		with TestClient(app) as client:
			gizur = {
				'name': 'gizur'
			}
			rsp = client.post('/users/', json=gizur)
			assert_equal(rsp.status_code, status.CREATED)
			data = rsp.json()
			assert_equal(data['name'], 'gizur')

	def test_get_user(self):
		with TestClient(app) as client:
			user = run_async(create_user)
			rsp = client.get('/user/%s' % user.id)
			assert_equal(rsp.status_code, status.OK)
			data = rsp.json()
			assert_dict_equal(
				data,
				{'id': user.id, 'name': user.name}
			)

	def test_get_all_users(self):
		with TestClient(app) as client:
			rsp = client.get('/users/')
			assert_equal(rsp.status_code, status.OK)
			data = rsp.json()
			assert_true('users' in data)
