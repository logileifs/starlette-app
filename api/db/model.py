import uuid

from rethinkdb import r
from rethinkdb import errors

import guid
import marshmallow
# from marshmallow import fields
# from marshmallow import Schema
from inflection import tableize

from api.db.connection import get_connection


class GUID(marshmallow.fields.Field):
	"""GUID field that uses a shortened (slug) version of a UUID"""

	def _deserialize(self, value, *args, **kwargs):
		try:
			guid.slug_to_uuid(value)
			return value
		except Exception:
			raise marshmallow.ValidationError("Not a valid id")

	def _serialize(self, value, *args, **kwargs):
		return str(value)


class ModelBase(type):
	def __new__(cls, clsname, bases, dct):
		super_new = super(ModelBase, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)

		fields_copy = {}
		new_class._fields = {}
		dct['id'] = GUID(missing=str(guid.GUID().slug))
		for key, value in dct.items():
			if not key.startswith('__'):
				new_class._fields[key] = value
				fields_copy[key] = value

		new_class._table = tableize(clsname)
		new_class._table_exists = False

		new_class._schema = marshmallow.Schema.from_dict(
			fields_copy,
			name=clsname + 'Schema'
		)
		return new_class


# @add_metaclass(ModelBase)
class Model(metaclass=ModelBase):

	def __init__(self, saved=False, *args, **kwargs):
		self.__dict__['_data'] = {}
		self.__dict__['_saved'] = saved
		data = self.load(kwargs)
		for key, value in data.items():
			setattr(self, key, value)

	def __setattr__(self, key, value):
		field = self._fields.get(key, None)
		if field:
			self._data[key] = value
			self.__dict__[key] = value
		super(Model, self).__setattr__(key, value)

	def validate(self, data=None):
		if data is None:
			data = self.dump(self._data)
		errors = self._schema().validate(data)
		if errors:
			raise marshmallow.exceptions.ValidationError(errors)

	def get_table(self):
		table = r.table(self._table)
		return table

	@property
	def data(self):
		return self._data

	@classmethod
	async def create_table(cls):
		connection = get_connection()
		result = await r.table_create(cls._table).run(connection)
		return result

	@classmethod
	async def all(cls, raw=False):
		connection = get_connection()
		table = r.table(cls._table)
		users = await table.run(connection)
		async for user in users:
			if raw:
				yield user
			else:
				yield cls(saved=True, **user)

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
				return cls(saved=True, **result)

	@classmethod
	def load(cls, data):
		return cls._schema().load(data)

	@classmethod
	def dump(cls, data):
		return cls._schema().dump(data)

	async def _do_insert(self):
		connection = get_connection()
		data = self.dump(self._data)
		self.validate(data)
		table = self.get_table()
		result = await table.insert(data, return_changes=True).run(connection)
		return result

	async def _do_update(self):
		connection = get_connection()
		data = self.dump(self._data)
		self.validate(data)
		table = self.get_table()
		result = await table.get(data['id']).update(
			data, non_atomic=True
		).run(connection)
		return result

	async def insert(self):
		try:
			result = await self._do_insert()
		except errors.ReqlOpFailedError:
			await self.create_table()
			result = await self._do_insert()
		return result

	async def update(self):
		try:
			result = await self._do_update()
		except errors.ReqlOpFailedError:
			await self.create_table()
			result = await self._do_update()
		return result

	async def save(self):
		if self._saved:
			result = await self.update()
		else:
			result = await self.insert()
		return result
