import datetime as dt

from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from api.db import Model
from api.db import fields

from guid import GUID


class User(Model):
	name = fields.Str()
	email = fields.Email(default='example@example.com')
	joined = fields.DateTime(missing=dt.datetime.utcnow())

class UserSchema(Schema):
	id = fields.Str(missing=str(GUID()))
	name = fields.Str()
	email = fields.Email()
	created_at = fields.DateTime()

	@post_load
	def make_user(self, data, **kwargs):
		return User(**data)
