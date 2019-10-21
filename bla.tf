# Set the variable value in *.tfvars file
# or using -var="do_token=..." CLI option
variable "do_token" { default = "00c871aac3376cbf40597bace97e5caf060c68e308e8ade8d9632f55e91fd961" }

# Configure the DigitalOcean Provider
provider "digitalocean" {
  token = "${var.do_token}"
}

# Create a web server
resource "digitalocean_droplet" "web" {
    image  = "ubuntu-18-04-x64"
    name   = "node1"
    region = "lon1"
    size   = "s-1vcpu-1gb"
}
#resource "dockermachine_digitalocean" "node" {
#resource "digitalocean_droplet" "web" {
#    count = 2
#    name = "${format("node-%02d", count.index+1)}"
#    cpu_count = 2
#    memory = 1024
#    
#    provisioner "remote-exec" {
#        inline = [
#            "touch /tmp/this_is_a_test",
#        ]
#        connection {
#            type        = "ssh"
#            host        = "${self.ssh_hostname}"
#            port        = "${self.ssh_port}"
#            user        = "${self.ssh_username}"
#            private_key = "${file("${self.ssh_keypath}")}"
#        }
#    }
#}