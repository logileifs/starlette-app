from marshmallow import Schema
#from marshmallow import fields
from marshmallow import post_load

from guid import GUID

from api.db import Model
from api.db import fields


class BaseSchema(Schema):
	@post_load
	def make_obj(self, data, **kwargs):
		return self._model(**data)


class OrganizationModel(Model):
	_table = 'organizations'

	def __init__(self, *args, **kwargs):
		#print('org __init__')
		#print('args: %s' % args)
		#print('kwargs: %s' % kwargs)
		for k, v in kwargs.items():
			setattr(self, k, v)


class OrganizationSchema(BaseSchema):
	_model = OrganizationModel
	name = fields.Str(required=True)
	id = fields.Str(missing=str(GUID()))

	#@post_load
	#def make_org(self, data, **kwargs):
	#	return OrganizationModel(**data)


#class Organization(Model):
#
#	def __new__(cls, **kwargs):
#		org = OrganizationSchema().load(kwargs)
#		return org

class Organization(Model):
	name = fields.String()
