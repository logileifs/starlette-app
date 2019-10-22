import names
import docker
import machine

m = machine.Machine()
client = docker.APIClient()
client.ping()

do_token = '<CHANGE ME>'

args = {
	'digitalocean-size': '1vcpu-1gb',
	'digitalocean-access-token': do_token,
	'digitalocean-region': 'lon1',
	'digitalocean-image': 'docker-18-04'
}

#['--digitalocean-size=s-1vcpu-1gb', '--digitalocean-access-token=<CHANGE ME>', '--digitalocean-region=lon1', '--digitalocean-image=docker-18-04']
xargs = ['--' + key + '=' + value for key, value in args.items()]
print('xargs: %s' % xargs)

#for n in number:
#	c = m.create(names.get_full_name().replace(' ', ''), driver='digitalocean', xarg=xargs)
#	#m.create(
#	#	names.get_full_name().replace(' ', ''),
#	#	driver='digitalocean',
#	#	xarg=[
#	#		'--digitalocean-region=lon1',
#	#		'--digitalocean-access-token=%s' % do_token
#	#	]
#	#)
