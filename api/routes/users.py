import logging
from http import HTTPStatus as status

from starlette.endpoints import HTTPEndpoint
from starlette.responses import UJSONResponse

#from webargs_starlette import use_kwargs
from webargs_starlette import use_args
from webargs import fields

from api.schemas.user import User

log = logging.getLogger(__name__)

new_user = {
	"name": fields.Str(required=True),
}


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

	@use_args(new_user)
	async def post(self, request, user):
		try:
			u = User(name=user['name'])
			u.save()
		except Exception:
			print('something horrible happened')
		return UJSONResponse(u.data, status_code=status.CREATED)
