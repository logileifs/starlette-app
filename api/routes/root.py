from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse
from starlette.responses import FileResponse
from starlette.authentication import requires


class Root(HTTPEndpoint):
	path = '/'

	@requires('authenticated')
	async def get(self, request):
		response = FileResponse('api/html/hello.html', media_type='html')
		return response
		#return UJSONResponse({'hello': 'world'})

	async def post(self, request):
		return UJSONResponse({'you': 'posted'})
