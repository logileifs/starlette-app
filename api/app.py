from starlette.routing import Router
from starlette.routing import Route
from starlette.config import Config
from starlette.applications import Starlette
from starlette import authentication as auth
from starlette.middleware.authentication import AuthenticationMiddleware

import guid
import base64
import logging
import uvicorn
import binascii
from api import db
from cryptography.fernet import Fernet

from api.routes.root import Root
from api.routes.other import signup_get
from api.routes.other import signup_post
from api.routes.user import UserEndpoint
from api.routes.users import UsersEndpoint
from api.misc.redislogger import RedisHandler


config = Config(".env")
DEBUG = config('DEBUG', cast=bool, default=False)
DB_HOST = config('DB_HOST', cast=str)
DB_NAME = config('DB_NAME', cast=str)
REDIS_HOST = config('REDIS_HOST', cast=str)
SECRET_KEY = config('SECRET_KEY', cast=str)

app = Starlette(debug=DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
rh = RedisHandler('logs', host=REDIS_HOST, level=logging.DEBUG)
rh.setLevel(logging.DEBUG)
log.addHandler(rh)
fernet_key = Fernet(SECRET_KEY)
#log.debug('DEBUG: %s' % DEBUG)


class BasicAuthBackend(auth.AuthenticationBackend):
	async def authenticate(self, request):
		log.info('authenticate')
		log.debug('headers: %s' % request.headers)
		if "Authorization" not in request.headers:
			log.error('missing authorization header')
			return

		auth_header = request.headers["Authorization"]
		log.debug('auth header: %s' % auth_header)
		try:
			scheme, credentials = auth_header.split()
			log.debug('scheme: %s' % scheme)
			log.debug('credentials: %s' % credentials)
			if scheme.lower() != 'token':
				return
			#decoded = base64.b64decode(credentials).decode("ascii")
			user_id = fernet_key.decrypt(credentials.encode())
			log.debug('user_id: %s' % user_id)
		except (ValueError, UnicodeDecodeError, binascii.Error) as exc:
			log.exception(exc)
			raise auth.AuthenticationError('Invalid basic auth credentials')

		#username, _, password = decoded.partition(":")
		# TODO: You'd want to verify the username and password here,
		#       possibly by installing `DatabaseMiddleware`
		#       and retrieving user information from `request.database`.
		return auth.AuthCredentials(["authenticated"]), auth.SimpleUser(user_id)


@app.middleware("http")
async def add_custom_header(request, call_next):
	request_headers = request.headers
	log.debug('headers: %s' % request_headers)
	log.debug('type(headers): %s' % type(request_headers))
	request.id = guid.GUID().slug
	log.debug('request.id: %s' % request.id)
	response = await call_next(request)
	response.headers['X-Request-ID'] = request.id
	return response


@app.on_event('startup')
async def before_startup():
	log.info('connecting to %s:28015/%s' % (DB_HOST, DB_NAME))
	await db.connect(host=DB_HOST, db=DB_NAME)
	log.debug('SECRET_KEY: %s' % SECRET_KEY)
	log.info('db connected')


@app.on_event('shutdown')
async def before_shutdown():
	await db.disconnect()


app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend())
app.add_route('/signup', signup_get, methods=["GET"])
app.add_route('/signup', signup_post, methods=["POST"])
router = Router(routes=[
	Route('/', endpoint=Root),
	Route('/users/', endpoint=UsersEndpoint),
	Route('/user/{id}', endpoint=UserEndpoint),
])
app.mount("", router)


if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8989)
