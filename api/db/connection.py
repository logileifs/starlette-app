from rethinkdb import r
from rethinkdb import errors

connections = []


class ConnectionError(Exception):
	pass


async def connect(**kwargs):
	host = kwargs.get('host', 'localhost')
	port = kwargs.get('port', 28015)
	db = kwargs.get('db', 'test')
	auth_key = kwargs.get('auth_key', None)
	user = kwargs.get('user', 'admin')
	password = kwargs.get('password', None)
	timeout = kwargs.get('timeout', 20)
	ssl = kwargs.get('ssl', {})
	handshake_version = kwargs.get('_handshake_version', 10)
	try:
		r.set_loop_type('asyncio')
		conn = await r.connect(
			host=host,
			port=port,
			db=db,
			auth_key=auth_key,
			user=user,
			password=password,
			timeout=timeout,
			ssl=ssl,
			_handshake_version=handshake_version,
		)
	except errors.RqlDriverError:
		raise ConnectionError('Could not connect to %s:%d/%s' % (host, port, db))

	try:
		result = await r.db_create(db).run(conn)
		# we will probably need to return the result to someone interested
	except errors.ReqlOpFailedError:
		#print('db already exists')
		pass
	connections.append(conn)
	return conn
	#r.connect(host=host, db=db, port=port, auth_key=auth_key)


async def disconnect():
	for conn in connections:
		await conn.close()


def get_connection():
	try:
		return connections[-1]
	except IndexError:
		raise ConnectionError('No open connection')
