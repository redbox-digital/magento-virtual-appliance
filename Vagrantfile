# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/centos-6.5"

  config.vm.network "private_network", ip: "10.3.118.121"

  # Increase ram of guest for mysql
  config.vm.provider "virtualbox" do |v|
      v.memory = 1024
  end

  # Use host SSH key for authentication to Github, etc.
  config.ssh.forward_agent = true

  # We don't want the default vagrant shared folder
  config.vm.synced_folder ".", "/vagrant",
    disabled: true

  config.vm.provision "file",
    source: "server-config",
    destination: "/tmp/server-config"

  # Base provisioning, things like installing servers and runtimes.
  config.vm.provision "shell",
    path: "base_provision.sh"

  # Project specific provisioning, installing projects and databases.
  config.vm.provision "shell",
    path: "project_provision.sh",
    privileged: false

  # Link only the vendor directory.
  #
  # If someone wants to view core code, check Bitbucket.
  config.vm.synced_folder "project", "/var/www/magento",
    type: "rsync"

end
