import logging

from starlette import authentication as auth
from cryptography.fernet import Fernet

from api.config import config

log = logging.getLogger(__name__)
fernet_key = Fernet(config.get('SECRET_KEY'))


class AuthBackend(auth.AuthenticationBackend):
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
		except (ValueError, UnicodeDecodeError) as exc:
			log.exception(exc)
			raise auth.AuthenticationError('Invalid basic auth credentials')

		#username, _, password = decoded.partition(":")
		# TODO: You'd want to verify the username and password here,
		#       possibly by installing `DatabaseMiddleware`
		#       and retrieving user information from `request.database`.
		return auth.AuthCredentials(["authenticated"]), auth.SimpleUser(user_id)
