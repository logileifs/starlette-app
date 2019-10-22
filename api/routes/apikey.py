import logging
from guid import GUID

from starlette.endpoints import HTTPEndpoint
from starlette.responses import FileResponse
from starlette.responses import UJSONResponse
from starlette.authentication import requires

from webargs import fields
from webargs_starlette import use_args


user_id = {
	"id": fields.Str(required=True),
}

log = logging.getLogger(__name__)


class ApiKey(HTTPEndpoint):
	path = '/apikey/'

	@requires('authenticated')
	async def get(self, request):
		response = FileResponse('api/html/hello.html', media_type='html')
		return response
		#return UJSONResponse({'hello': 'world'})

	@use_args(user_id)
	async def post(self, request):
		log.info('create new api key for user %s' % user_id)
		return UJSONResponse({'apikey': GUID().slug})
