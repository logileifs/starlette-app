from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse
from starlette.responses import FileResponse


class Root(HTTPEndpoint):
	path = '/'

	async def get(self, request):
		response = FileResponse('api/html/hello.html', media_type='html')
		return response
		#return UJSONResponse({'hello': 'world'})

	async def post(self, request):
		return UJSONResponse({'you': 'posted'})
