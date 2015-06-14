# vi: set ft=ruby
#

Vagrant.configure("2") do |config|
    config.vm.define "vagrant" # for ansible inventory

    config.vm.box = "trusty64"
    config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"

    config.vm.network :forwarded_port, guest: 8000, host: 8000

    config.vm.provision "ansible" do |ansible|
        ansible.playbook = "provision/site.yml"
    end
end
