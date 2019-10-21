from marshmallow import Schema, fields


class User:
	def __init__(self, name, org=None):
		self.name = name
		self.org = org


class UserSchema(Schema):
	name = fields.String()
	org = fields.Nested('OrgSchema')


class Org:
	def __init__(self, name):
		self.name = name


class OrgSchema(Schema):
	name = fields.String()


"""
	def serialize(self, attr, obj, accessor=None, **kwargs):
		(Pdb) self
			<fields.Nested(
				default=<marshmallow.missing>,
				attribute=None,
				validate=None,
				required=False,
				load_only=False,
				dump_only=False,
				missing=<marshmallow.missing>,
				allow_none=False,
				error_messages={
					'required': 'Missing data for required field.',
					'null': 'Field may not be null.',
					'validator_failed': 'Invalid value.',
					'type': 'Invalid type.'
				}
			)>
		(Pdb) attr
			'org'
		(Pdb) obj
			<__main__.User object at 0x7f277beb7780>

	def get_value(self, obj, attr, accessor=None, default=missing_):
		(Pdb) self
			<fields.Nested(
				default=<marshmallow.missing>,
				attribute=None,
				validate=None,
				required=False,
				load_only=False,
				dump_only=False,
				missing=<marshmallow.missing>,
				allow_none=False,
				error_messages={
					'required': 'Missing data for required field.',
					'null': 'Field may not be null.',
					'validator_failed': 'Invalid value.',
					'type': 'Invalid type.'
				}
			)>
		(Pdb) obj
			<__main__.User object at 0x7f277beb7780>
		(Pdb) attr
			'org'
		(Pdb) accessor
			<bound method BaseSchema.get_attribute of <UserSchema(many=False)>>
"""


if __name__ == '__main__':
	grid = Org(name='grid')
	krilli = User(name='krilli', org=grid)
	UserSchema().dump(krilli)
