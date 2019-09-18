import logging

from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

#from webargs_starlette import use_kwargs
#from webargs import fields

from api.schemas.user import User

log = logging.getLogger(__name__)

class UsersEndpoint(HTTPEndpoint):
	path = '/users/'

	async def get(self, request):
		users = User.all(raw=True)
		rsp = {'users': []}
		async for user in users:
			log.debug('user: %s' % user)
			rsp['users'].append(user)
		print('rsp: %s' % rsp)
		return UJSONResponse(rsp)
