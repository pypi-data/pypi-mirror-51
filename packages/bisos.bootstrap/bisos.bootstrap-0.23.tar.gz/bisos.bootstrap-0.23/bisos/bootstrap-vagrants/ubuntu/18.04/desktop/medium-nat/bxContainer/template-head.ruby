# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.define "{vmName}" do |guest|
    guest.vm.box = "peru/ubuntu-18.04-desktop-amd64"
    guest.vm.hostname = "{vmName}"
    guest.vm.provider :virtualbox do |vb|
      vb.memory = "1024"		  
    end

    ## SHELL PROVISIONING
    guest.vm.provision "shell", inline: <<-_EOF_MainRootShell_
