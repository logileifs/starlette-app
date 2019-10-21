from marshmallow import Schema, fields, pprint
from marshmallow.schema import SchemaMeta

from six import with_metaclass


class Model:
	pass


class SchemaMeta(SchemaMeta):
	def __new__(cls, clsname, bases, dct):
		print('SchemaMeta __new__')
		super_new = super(SchemaMeta, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)

		model_fields = {'field1': 'value1', 'field2': 'value2'}
		new_class._model = type(
			clsname + 'Model',
			(Model,),
			model_fields
		)
		return new_class


class ModelMeta(type):
	def __new__(cls, clsname, bases, dct):
		super_new = super(ModelMeta, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)
		return new_class


#class ModelSchema(Schema):
class ModelSchema(with_metaclass(SchemaMeta, Schema)):

	def make_object(self):
		#new_class._schema = type(
		#	clsname + 'Schema',
		#	(marshmallow.Schema,),
		#	fields_copy
		#)
		pass


class UserSchema(ModelSchema):
	name = fields.String()
	org = fields.Nested('OrgSchema')
	#email = fields.Email()
	#created_at = fields.DateTime()


class OrgSchema(ModelSchema):
	name = fields.String()
	#author = fields.Nested(UserSchema)
