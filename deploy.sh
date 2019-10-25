docker-machine create --driver digitalocean --digitalocean-size s-1vcpu-1gb --digitalocean-region lon1 --digitalocean-image ubuntu-18-04-x64 --digitalocean-access-token '<CHANGE ME>' node1
docker-machine create --driver digitalocean --digitalocean-size s-1vcpu-1gb --digitalocean-region lon1 --digitalocean-image ubuntu-18-04-x64 --digitalocean-access-token '<CHANGE ME>' node2
docker-machine create --driver digitalocean --digitalocean-size s-1vcpu-1gb --digitalocean-region lon1 --digitalocean-image ubuntu-18-04-x64 --digitalocean-access-token '<CHANGE ME>' node3

docker-machine ssh node1 'ufw allow 22/tcp'
docker-machine ssh node1 'ufw allow 2376/tcp'
docker-machine ssh node1 'ufw allow 2377/tcp'
docker-machine ssh node1 'ufw allow 7946/tcp'
docker-machine ssh node1 'ufw allow 7946/udp'
docker-machine ssh node1 'ufw allow 4789/udp'
docker-machine ssh node1 'echo "y" | ufw enable'
docker-machine ssh node1 'systemctl restart docker'

docker-machine ssh node2 'ufw allow 22/tcp'
docker-machine ssh node2 'ufw allow 2376/tcp'
docker-machine ssh node2 'ufw allow 7946/tcp'
docker-machine ssh node2 'ufw allow 7946/udp'
docker-machine ssh node2 'ufw allow 4789/udp'
docker-machine ssh node2 'echo "y" | ufw enable'
docker-machine ssh node2 'systemctl restart docker'

docker-machine ssh node3 'ufw allow 22/tcp'
docker-machine ssh node3 'ufw allow 2376/tcp'
docker-machine ssh node3 'ufw allow 7946/tcp'
docker-machine ssh node3 'ufw allow 7946/udp'
docker-machine ssh node3 'ufw allow 4789/udp'
docker-machine ssh node3 'echo "y" | ufw enable'
docker-machine ssh node3 'systemctl restart docker'

eval $(docker-machine env node1)

docker-machine ssh node1 "'docker swarm init --advertise-addr $(docker-machine ip node1)'"
docker-machine ssh node2 "'docker swarm join --token $(docker swarm join-token worker --quiet) $(docker-machine ip node1):2377'"
docker-machine ssh node3 "'docker swarm join --token $(docker swarm join-token worker --quiet) $(docker-machine ip node1):2377'"

docker stack deploy -c docker-compose.yml node1
eval $(docker-machine env --unset)