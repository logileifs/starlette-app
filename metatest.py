import uuid
import inspect
import marshmallow as ma
from six import add_metaclass
from inflection import tableize
from collections import OrderedDict

class MetaA(type):
	pass

class MetaB(type):
	pass

#@add_metaclass(MetaA)
class BaseA(metaclass=MetaA):
	pass

#@add_metaclass(MetaB)
class BaseB(metaclass=MetaB):
	pass

class MetaAB(MetaA, MetaB):
	pass

#@add_metaclass(MetaAB)
class Fixed(BaseA, BaseB, metaclass=MetaAB):
	pass

class ModelBase(type):
	def __new__(cls, clsname, bases, dct):
		super_new = super(ModelBase, cls).__new__
		new_class = super_new(cls, clsname, bases, dct)

		fields_copy = {}
		new_class._fields = {}
		for key, value in dct.items():
			print('%s: %s' % (key, value))
			if not key.startswith('__'):
				new_class._fields[key] = value
				fields_copy[key] = value

		new_class._table = tableize(clsname)
		new_class._table_exists = False

		fields_copy['id'] = ma.fields.UUID(required=True)
		new_class._schema = type(
			clsname + 'Schema',
			(ma.Schema,),
			fields_copy
		)
		return new_class


#@add_metaclass(ModelBase)
class Model(metaclass=ModelBase):
	def __init__(self, saved=False, *args, **kwargs):
		self.__dict__['_data'] = {}
		self.__dict__['_saved'] = saved
		for key, value in kwargs.items():
			print('for %s, %s' % (key, value))
			setattr(self, key, value)
		if 'id' not in self._data:
			setattr(self, 'id', str(uuid.uuid4()))

	def __setattr__(self, key, value):
		print('__setattr__')
		field = self._fields.get(key, None)
		if field:
			#if self._get_value(key) != value:
			#	self._dirty = True
			self._data[key] = value
			self.__dict__[key] = value
		super(Model, self).__setattr__(key, value)

	def _do_insert(self):
		connection = get_connection()
		table = self.get_table()
		result = table.insert(self._data, return_changes=True).run(connection)
		errors = result['errors']
		if not errors:
			self._data['id'] = result['generated_keys'][0]
		return result

	def _do_update(self):
		print('do update')
		connection = get_connection()
		table = self.get_table()
		_id = self._data['id']
		print('data: %s' % self._data)
		result = table.get(_id).update(
			self._data, non_atomic=True
		).run(connection)
		return result


	def insert(self):
		try:
			result = self._do_insert()
		except r.errors.ReqlOpFailedError:
			self.create_table()
			result = self._do_insert()
		return result

	def update(self):
		try:
			result = self._do_update()
		except r.errors.ReqlOpFailedError:
			self.create_table()
			result = self._do_update()
		return result

	def save(self):
		try:
			result = self.update()
		except KeyError:
			result = self.insert()
		return result
