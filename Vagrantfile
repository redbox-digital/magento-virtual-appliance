# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/centos-6.5"

  config.vm.synced_folder ".", "/vagrant",
    disabled: true

  config.vm.provision "file",
    source: "server-config",
    destination: "/tmp/server-config"

  # Base provisioning, things like installing servers and runtimes.
  config.vm.provision "shell",
    path: "base_provision.sh"

end
