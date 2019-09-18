import uuid

from rethinkdb import r
from rethinkdb import errors

import marshmallow
from marshmallow import fields
#from marshmallow import Schema
from inflection import tableize

from api.db.connection import get_connection


class ModelBase(type):
	def __new__(cls, clsname, bases, dct):
		super_new = super(ModelBase, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)

		fields_copy = {}
		new_class._fields = {}
		for key, value in dct.items():
			if not key.startswith('__'):
				new_class._fields[key] = value
				fields_copy[key] = value

		new_class._fields['id'] = marshmallow.fields.UUID(required=True)
		new_class._table = tableize(clsname)
		new_class._table_exists = False

		fields_copy['id'] = marshmallow.fields.UUID(required=True)
		#new_class._schema = type(
		#	clsname + 'Schema',
		#	(marshmallow.Schema,),
		#	fields_copy
		#)
		new_class._schema = marshmallow.Schema.from_dict(
			fields_copy,
			name=clsname + 'Schema'
		)
		return new_class


#@add_metaclass(ModelBase)
class Model(metaclass=ModelBase):
	def __init__(self, saved=False, *args, **kwargs):
		self.__dict__['_data'] = {}
		self.__dict__['_saved'] = saved
		for key, value in kwargs.items():
			setattr(self, key, value)
		if 'id' not in self._data:
			setattr(self, 'id', str(uuid.uuid4()))

	def __setattr__(self, key, value):
		field = self._fields.get(key, None)
		if field:
			self._data[key] = value
			self.__dict__[key] = value
		super(Model, self).__setattr__(key, value)

	def validate(self):
		errors = self._schema().validate(self._data)
		if errors:
			raise marshmallow.exceptions.ValidationError(errors)

	def get_table(self):
		table = r.table(self._table)
		return table

	@property
	def data(self):
		return self._data

	@classmethod
	def create_table(self):
		connection = get_connection()
		r.table_create(self._table).run(connection)

	@classmethod
	async def all(cls, raw=False):
		connection = get_connection()
		table = r.table(cls._table)
		users = await table.run(connection)
		async for user in users:
			if raw:
				yield user
			else:
				yield cls.load(user)

	@classmethod
	async def get(cls, _id, raw=False):
		connection = get_connection()
		table = r.table(cls._table)
		result = await table.get(_id).run(connection)
		if raw:
			return result
		else:
			if result is None:
				return result
			else:
				print('return cls._schema.load(%s)' % result)
				return cls.load(result)

	@classmethod
	def load(cls, data):
		result = cls._schema().load(data)
		return cls(**result)

	async def _do_insert(self):
		connection = get_connection()
		table = self.get_table()
		result = await table.insert(self._data, return_changes=True).run(connection)
		return result

	async def _do_update(self):
		connection = get_connection()
		table = self.get_table()
		_id = self._data['id']
		result = await table.get(_id).update(
			self._data, non_atomic=True
		).run(connection)
		return result

	async def insert(self):
		self.validate()
		try:
			result = await self._do_insert()
		except errors.ReqlOpFailedError:
			self.create_table()
			result = await self._do_insert()
		return result

	async def update(self):
		self.validate()
		try:
			result = await self._do_update()
		except errors.ReqlOpFailedError:
			self.create_table()
			result = await self._do_update()
		return result

	async def save(self):
		self.validate()
		if self._saved:
			result = await self.update()
		else:
			result = await self.insert()
		return result
