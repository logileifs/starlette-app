import datetime as dt

from marshmallow import Schema
from marshmallow import fields
from marshmallow import post_load

from api.db import Model
from api.db import fields

from guid import GUID


class User(Model):
	name = fields.Str(required=True)
	email = fields.Email(default='example@example.com')
	joined = fields.DateTime(missing=dt.datetime.utcnow())
