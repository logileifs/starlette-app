import logging

from webargs import fields
from marshmallow import ValidationError
from webargs_starlette import use_kwargs
from starlette.responses import HTMLResponse

from api.schemas.organization import Organization

log = logging.getLogger(__name__)


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
		""".replace('\t', '')
	return HTMLResponse(html)


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
		log.info('org: %s' % org)
	except ValidationError:
		log.info('invalid org')
		return HTMLResponse(error_rsp)
	try:
		#await r.table('organizations').insert({'name': org}).run(connection)
		await org.save()
		#await r.table('users').insert({'name': name, 'email': email}).run(connection)
	except Exception as ex:
		log.info('error inserting to database!')
		log.info('ex: %s' % ex)
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
