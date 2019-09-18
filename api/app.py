from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Router
from starlette.routing import Route

from webargs import fields
from webargs_starlette import use_kwargs
from marshmallow import ValidationError


import uvicorn
from rethinkdb import r
from api.db.connection import connect
from api.db.connection import disconnect

from api.routes.root import Root
from api.routes.user import UserEndpoint
from api.routes.users import UsersEndpoint
#from api.importer import import_routes
from api.schemas.organization import Organization


app = Starlette(debug=True)


@app.on_event('startup')
async def before_startup():
	await connect(db='test')


@app.on_event('shutdown')
async def before_shutdown():
	await disconnect()


router = Router(routes=[
	Route('/', endpoint=Root),
	Route('/users/', endpoint=UsersEndpoint),
	Route('/user/{id}', endpoint=UserEndpoint),
])
app.mount("", router)


@app.route('/signup', methods=['get'])
async def signup_get(request):
	html = """
		<!DOCTYPE html>
		<html>
			<head>
				<title>Sign up!</title>
			</head>
			<body>
				<h1>The Company</h1>
				<form action="/signup" method="post">
					Organization: <input type="text" name="org"><br>
					Name: <input type="text" name="name"><br>
					Email: <input type="text" name="email"><br>
					<input type="submit" value="Submit">
				</form>
			</body>
		</html>
		"""
	return HTMLResponse(html)


@app.route('/signup', methods=['post'])
@use_kwargs(
	{
		"name": fields.Str(required=True),
		"org": fields.Str(required=True),
		"email": fields.Str(required=True)
	}
)
async def signup_post(request, name, org, email):
	error_rsp = """
		<!DOCTYPE html>
		<html>
			<head>
				<title>Sign up!</title>
			</head>
			<body>
				<h1>Oops! something went wrong :/</h1>
			</body>
		</html>
		"""
	try:
		org = Organization(name=org)
		print('org: %s' % org)
	except ValidationError:
		print('invalid org')
		return HTMLResponse(error_rsp)
	try:
		#await r.table('organizations').insert({'name': org}).run(connection)
		org.save()
		await r.table('users').insert({'name': name, 'email': email}).run(connection)
	except Exception as ex:
		print('error inserting to database!')
		print('ex: %s' % ex)
		return HTMLResponse(error_rsp)
	html = """
		<!DOCTYPE html>
		<html>
			<head>
				<title>Sign up!</title>
			</head>
			<body>
				<h1>Thank you!</h1>
			</body>
		</html>
	"""
	return HTMLResponse(html)


if __name__ == '__main__':
	uvicorn.run(app, host='0.0.0.0', port=8989)
