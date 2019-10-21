from rethinkdb import r
from rethinkdb import errors

import guid
import marshmallow as ma
# from marshmallow import fields
# from marshmallow import Schema
from inflection import tableize

from api.db.connection import get_connection


#class SchemaMeta(ma.schema.SchemaMeta):
#	"""Metaclass for `ModelSchema`."""
#	pass


#class ModelSchema(with_metaclass(SchemaMeta, ma.Schema)):
#	pass


class ModelSchema(ma.Schema):

	@ma.pre_dump
	def _pre_dump(self, data, many, **kwargs):
		print('pre_dump data: %s' % data)
		pre_processed = {}
		for key, value in data.items():
			if isinstance(value, Model):
				print('pre_dump got Model object: %s' % value)
				pre_processed[key] = value.id
			else:
				pre_processed[key] = value
		return pre_processed
		#to_skip = self.opts.model_skip_values
		#return {
		#	key: value for key, value in data.items()
		#	if value not in to_skip
		#}


class GUID(ma.fields.Field):
	"""GUID field that uses a shortened (slug) version of a UUID"""

	def _deserialize(self, value, *args, **kwargs):
		try:
			guid.slug_to_uuid(value)
			return value
		except Exception:
			raise ma.ValidationError("Not a valid id")

	def _serialize(self, value, *args, **kwargs):
		return str(value)


class ModelBase(type):
	def __new__(cls, clsname, bases, dct):
		super_new = super(ModelBase, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)

		fields_copy = {}
		new_class._fields = {}
		dct['id'] = GUID(missing=lambda: str(guid.GUID().slug))
		for key, value in dct.items():
			if not key.startswith('__'):
				new_class._fields[key] = value
				fields_copy[key] = value

		new_class._table = tableize(clsname)
		new_class._table_exists = False

		new_class._schema = ma.Schema.from_dict(
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
			data = self.dump(self)
		errors = self._schema().validate(data)
		if errors:
			raise ma.exceptions.ValidationError(errors)

	@property
	def data(self):
		return self._data

	@property
	def saved(self):
		return self._saved

	@classmethod
	def load(cls, data):
		return cls._schema().load(data)

	@classmethod
	def dump(cls, obj):
		#print('dumping obj: %s' % obj)
		return cls._schema().dump(obj)

	@classmethod
	def get_table(cls):
		table = r.table(cls._table)
		return table

	@classmethod
	async def create_table(cls):
		connection = get_connection()
		result = await r.table_create(cls._table).run(connection)
		return result

	@classmethod
	async def all(cls, raw=False):
		connection = get_connection()
		table = cls.get_table()
		try:
			users = await table.run(connection)
		except errors.ReqlOpFailedError as err:
			yield None
		async for user in users:
			if raw:
				yield user
			else:
				yield cls(saved=True, **user)

	@classmethod
	async def get(cls, _id, raw=False):
		connection = get_connection()
		table = cls.get_table()
		result = await table.get(_id).run(connection)
		if raw:
			return result
		else:
			if result is None:
				return result
			else:
				return cls(saved=True, **result)

	@classmethod
	async def drop(cls):
		conn = get_connection()
		table = cls.get_table()
		result = await table.delete().run(conn)
		return result

	@classmethod
	def watch(cls):
		#connection = get_connection()
		#table = cls.get_table()
		#feed = table.changes().run(connection)
		#yield from feed
		raise NotImplemented("this code isn't working yet")

	async def _do_insert(self):
		connection = get_connection()
		data = self.dump(self._data)
		self.validate(data)
		table = self.get_table()
		result = await table.insert(data, return_changes=True).run(connection)
		return result

	async def _do_update(self):
		conn = get_connection()
		data = self.dump(self._data)
		self.validate(data)
		table = self.get_table()
		result = await table.get(data['id']).update(
			data, return_changes=True
		).run(conn)
		return result

	async def insert(self):
		try:
			result = await self._do_insert()
		except errors.ReqlOpFailedError:
			await self.create_table()
			result = await self._do_insert()
		self._saved = True
		return result

	async def update(self):
		try:
			result = await self._do_update()
		except errors.ReqlOpFailedError:
			await self.create_table()
			result = await self._do_update()
		return result

	async def delete(self):
		conn = get_connection()
		table = self.get_table()
		data = self.dump(self._data)
		try:
			res = await table.get(data['id']).delete(return_changes=True).run(conn)
		except errors.ReqlOpFailedError:
			return res
		self._saved = False
		return res

	async def save(self):
		if self._saved:
			result = await self.update()
		else:
			result = await self.insert()
		return result
