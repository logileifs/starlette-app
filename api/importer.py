from os import listdir
from importlib import import_module


def import_routes(app, directory):
	print('directory: %s' % directory)
	mods = listdir(directory)
	print('mods: %s' % mods)
	for mod in mods:
		if not mod.endswith('.py'):
			continue
		if mod.startswith('__init__'):
			continue
		m = import_module(directory.replace('/', '.') + '.' + mod.split('.py')[0])
		app.add_route(m.route)
