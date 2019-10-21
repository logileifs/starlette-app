import logging

from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

#from webargs_starlette import use_kwargs
#from webargs import fields

from api.schemas.user import User

log = logging.getLogger(__name__)


class UserEndpoint(HTTPEndpoint):
	path = '/user/{id}'

	async def get(self, request):
		user_id = request.path_params['id']
		log.info('get user with id: %s' % user_id)
		u = await User.get(user_id, raw=True)
		log.info('got user: %s' % u)
		return UJSONResponse(u)
