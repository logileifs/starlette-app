from http import HTTPStatus as status

import asynctest
from async_asgi_testclient import TestClient

from api.app import app
from tests.asserts import *


class TestOtherRoutes(asynctest.TestCase):

	async def test_signup_get(self):
		async with TestClient(app) as client:
			html = """
			<!DOCTYPE html>
			<html>
				<head>
					<title>Sign up!</title>
				</head>
				<body>
					<h1>The Company</h1>
					<form action="/signup" method="post">
						Organization: <input type="text" name="org"><br>
						Name: <input type="text" name="name"><br>
						Email: <input type="text" name="email"><br>
						<input type="submit" value="Submit">
					</form>
				</body>
			</html>
			""".replace('\t', '')
			rsp = await client.get('/signup')
			assert_equal(rsp.status_code, status.OK)
			request_id = rsp.headers['X-Request-ID']
			assert_not_none(request_id)
			assert_equal(rsp.content, html.encode())

	async def test_signup_post(self):
		async with TestClient(app) as client:
			rsp = await client.post('/signup')
			assert_not_equal(rsp.status_code, status.NOT_FOUND)
