import names
import docker
import machine

m = machine.Machine()
client = docker.APIClient()
client.ping()

do_token = '00c871aac3376cbf40597bace97e5caf060c68e308e8ade8d9632f55e91fd961'

args = {
	'digitalocean-size': '1vcpu-1gb',
	'digitalocean-access-token': do_token,
	'digitalocean-region': 'lon1',
	'digitalocean-image': 'docker-18-04'
}

#['--digitalocean-size=s-1vcpu-1gb', '--digitalocean-access-token=00c871aac3376cbf40597bace97e5caf060c68e308e8ade8d9632f55e91fd961', '--digitalocean-region=lon1', '--digitalocean-image=docker-18-04']
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
