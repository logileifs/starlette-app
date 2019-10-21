from api.db.model import Model
from api.db import fields


class Org(Model):
	name = fields.String()


class User(Model):
	name = fields.String()
	org = fields.Nested(Org)


if __name__ == '__main__':
	grid = Org(name='grid')
	krilli = User(name='krilli')
	#krilli.org = grid
	result = User.dump(krilli)
	print(result)
