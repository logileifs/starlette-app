from async_asgi_testclient import TestClient


class TestClient(TestClient):
	def __init__(self, *args, headers=None, **kwargs):
		super().__init__(*args, **kwargs)
		self.headers = headers

	async def open(
		self,
		path,
		*,
		method="GET",
		headers=None,
		data=None,
		form=None,
		query_string=None,
		json=None,
		scheme="http",
		cookies=None,
		stream=False,
		allow_redirects=True,
	):
		return await super().open(
			path,
			method=method,
			headers=self.headers,
			data=data,
			form=form,
			query_string=query_string,
			json=json,
			scheme=scheme,
			cookies=cookies,
			stream=stream,
			allow_redirects=allow_redirects
		)

# Example usage:
"""
client = TestClient(app)
client.headers = {
	'authorization': 'token mytoken'
}
"""
