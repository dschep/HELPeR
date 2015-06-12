# vi: set ft=ruby
#
$script = <<SCRIPT
apt-get update
apt-get install -y python-virtualenv python3-dev libpq-dev posgresql postgresql-contrib-9.3 rabitmq-server
sudo -u vagrant virtualenv --python=/usr/bin/python3 /home/vagrant/venv
sudo -u postgres createuser -s vagrant
sudo -u vagrant createdb helper
sudo -u vagrant psql -c "create extension if not exists hstore;"
SCRIPT

Vagrant.configure("2") do |config|
    config.vm.define "vagrant" # for ansible inventory

    config.vm.box = "trusty64"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    config.vm.network :forwarded_port, guest: 8000, host: 8000
end
