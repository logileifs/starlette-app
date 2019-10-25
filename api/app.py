from starlette.routing import Router
from starlette.routing import Route
from starlette.applications import Starlette

import guid
import logging
import uvicorn
from api import db

from api.config import config
from api.auth import AuthBackend
from api.routes.root import Root
from api.routes.other import signup_get
from api.routes.other import signup_post
from api.routes.user import UserEndpoint
from api.routes.users import UsersEndpoint
from api.misc.redislogger import RedisHandler
from starlette.middleware.authentication import AuthenticationMiddleware


app = Starlette(debug=config.get('DEBUG'))
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
rh = RedisHandler('logs', host=config.get('REDIS_HOST'), level=logging.DEBUG)
rh.setLevel(logging.DEBUG)
log.addHandler(rh)


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
	log.debug('DEBUG: %s' % config.get('DEBUG'))
	db_host = config.get('DB_HOST')
	db_name = config.get('DB_NAME')
	log.info('connecting to %s:28015/%s' % (db_host, db_name))
	await db.connect(host=db_host, db=db_name)
	log.debug('SECRET_KEY: %s' % config.get('SECRET_KEY'))
	log.info('db connected')


@app.on_event('shutdown')
async def before_shutdown():
	await db.disconnect()


app.add_middleware(AuthenticationMiddleware, backend=AuthBackend())
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
