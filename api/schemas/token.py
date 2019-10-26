from api.db import Model
from api.db import fields


class Token(Model):
	token = fields.String()
	user_id = fields.String()
