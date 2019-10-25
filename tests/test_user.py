import asyncio
from http import HTTPStatus as status

#from starlette.responses import HTMLResponse
#from starlette.testclient import TestClient

import asynctest
from async_asgi_testclient import TestClient

from api import db
from api.app import app
from api.app import before_startup
from api.app import before_shutdown
from api.schemas.user import User
from tests.asserts import *


async def create_user():
	await db.connect()
	u = User(name='glommi', email='glommi@glomm.is')
	await u.save()
	return u


def run_async(func):
	value = asyncio.get_event_loop().run_until_complete(func())
	return value


#class TestClient(async_asgi_testclient.TestClient):
#	def __init__(self, *args, headers=None, **kwargs):
#		super().__init__(*args, **kwargs)
#		self.headers = headers
#
#	async def open(self, *args, **kwargs):
#		return await super().open(*args, headers=self.headers, **kwargs)


client = TestClient(app)
#headers = {
#	'authorization': 'token gAAAAABdsjBsbm_5BRNITObSUYvn2v_F7lz4AuWPIK7L0eWr-5F3pUh0uRa6ExZL0OACgbuKQRJxWm9gOYxmM_jP0PFpnxDWIQ=='
#}
#client.headers = {'authorization': 'token mytoken'}


class MinimalExample(asynctest.TestCase):

	async def setUp(self):
		await before_startup()

	async def tearDown(self):
		await before_shutdown()

	async def test_app(self):
		response = await client.get('/')
		assert_equal(response.status_code, 200)
		request_id = response.headers['X-Request-ID']
		print('request_id: %s' % request_id)
		assert_not_none(request_id)

	async def test_create_user(self):
		gizur = {'name': 'gizur'}
		rsp = await client.post('/users/', json=gizur)
		assert_equal(rsp.status_code, status.CREATED)
		data = rsp.json()
		assert_equal(data['name'], 'gizur')

	async def test_get_user(self):
		user = await create_user()
		rsp = await client.get('/user/%s' % user.id)
		assert_equal(rsp.status_code, status.OK)
		data = rsp.json()
		assert_equal(data['id'], user.id)
		assert_equal(data['name'], user.name)

	async def test_get_all_users(self):
		rsp = await client.get('/users/')
		assert_equal(rsp.status_code, status.OK)
		data = rsp.json()
		assert_true('users' in data)
