Vagrant.configure("2") do |config|
  config.vm.define "{vmName}" do |guest|
    guest.vm.box = "peru/ubuntu-18.04-desktop-amd64"
    #guest.vm.box_version = "20181001.01"
    guest.vm.hostname = "{vmName}"
    guest.vm.provider :virtualbox do |vb|
      # Visual Basic GUI (NOT used to configure guest's Xwindows setup)
      #vb.gui = true
      # Define basics
      vb.customize ["modifyvm", :id, "--memory", 5120]
      vb.customize ["modifyvm", :id, "--cpus", 2]
      vb.customize ["modifyvm", :id, "--vram", 256]
      vb.customize ["modifyvm", :id, "--clipboard", "bidirectional"]
      vb.customize ["modifyvm", :id, "--draganddrop", "hosttoguest"]
      # For better DNS resolution
      vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
      # No audio
      vb.customize ["modifyvm", :id, "--audio", "none"]
      # For performance
      vb.customize ["modifyvm", :id, "--usb", "off"]
      # Huge performance gain here
      vb.linked_clone = true if Vagrant::VERSION >= '1.8.0'
    end

    ## SHELL PROVISIONING
    guest.vm.provision "shell", inline: <<-_EOF_MainRootShell_
