from starlette.responses import HTMLResponse
from starlette.testclient import TestClient

import asynctest
from http import HTTPStatus as status

from api.app import app
from tests.asserts import *


#client = TestClient(app)


class MinimalExample(asynctest.TestCase):
	def test_that_true_is_true(self):
		assert_true(True)

	def test_app(self):
		with TestClient(app) as client:
			response = client.get('/')
			assert_equal(response.status_code, 200)

	def test_get_user(self):
		with TestClient(app) as client:
			rsp = client.get('/user/de949483-4ee4-4b0e-a928-981ece4ced54')
			assert_equal(rsp.status_code, status.OK)
			data = rsp.json()
			assert_dict_equal(
				data,
				{'id': 'de949483-4ee4-4b0e-a928-981ece4ced54', 'name': 'gizur'}
			)

	def test_get_all_users(self):
		with TestClient(app) as client:
			rsp = client.get('/users/')
			assert_equal(rsp.status_code, status.OK)
			data = rsp.json()
			assert_true('users' in data)
			#print('data: %s' % data)
