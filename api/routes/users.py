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
		users = [u async for u in User.all(raw=True)]
		rsp = {'users': users}
		log.debug('rsp: %s' % rsp)
		return UJSONResponse(rsp)

	@use_args(new_user)
	async def post(self, request, new_user):
		try:
			u = User(name=new_user['name'])
			await u.save()
		except Exception:
			log.error('something horrible happened')
		return UJSONResponse(u.data, status_code=status.CREATED)
