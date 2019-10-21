#from starlette.responses import HTMLResponse
#from starlette.testclient import TestClient

import asyncio
import asynctest
from concurrent.futures import ThreadPoolExecutor

from rethinkdb import r
from rethinkdb import errors

#from app import app
from tests.asserts import *
from api import db



class DBTests(asynctest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.conn = r.connect()
		try:
			r.db_drop('test').run(cls.conn)
		except errors.ReqlOpFailedError:
			pass
		r.db_create('test').run(cls.conn)

	@classmethod
	def tearDownClass(cls):
		r.db_drop('test').run(cls.conn)
		cls.conn.close()

	async def setUp(self):
		#print('setUp')
		await db.connect()

	async def tearDown(self):
		await db.disconnect()
		#await asyncio.sleep(0)

	async def test_basic(self):
		class User(db.Model):
			name = db.fields.String()
		u = User(name='blommi')
		result = await u.save()
		errors = result['errors']
		#print('errors: %s' % errors)
		assert_equal(errors, 0)

	async def test_get_all_users(self):
		#print('test_get_all_users')
		class User(db.Model):
			name = db.fields.Str()
			email = db.fields.Email()
		user = User(name='lalli')
		await user.save()
		users = User.all()
		async for user in users:
			assert_true(isinstance(user, User))

	#def test_app(self):
	#	response = client.get('/')
	#	assert_equal(response.status_code, 200)
