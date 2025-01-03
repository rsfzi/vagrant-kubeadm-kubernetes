
require "yaml"
vagrant_root = File.dirname(File.expand_path(__FILE__))
settings = YAML.load_file "#{vagrant_root}/settings.yaml"

IP_SECTIONS = settings["network"]["control_ip"].match(/^([0-9.]+\.)([^.]+)$/)
# First 3 octets including the trailing dot:
IP_NW = IP_SECTIONS.captures[0]
# Last octet excluding all dots:
IP_START = Integer(IP_SECTIONS.captures[1])
NUM_WORKER_NODES = settings["nodes"]["workers"]["count"]
WORKER_PREFIX = ""
if settings["nodes"]["workers"]["prefix"]
  WORKER_PREFIX = settings["nodes"]["workers"]["prefix"]
end

Vagrant.configure("2") do |config|
  config.vm.provision "shell", env: { "IP_NW" => IP_NW, "IP_START" => IP_START, "NUM_WORKER_NODES" => NUM_WORKER_NODES }, inline: <<-SHELL
      apt-get update -y
      echo "$IP_NW$((IP_START)) controlplane" >> /etc/hosts
      for i in `seq 1 ${NUM_WORKER_NODES}`; do
        echo "$IP_NW$((IP_START+i)) $WORKER_PREFIXnode0${i}" >> /etc/hosts
      done
  SHELL
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get install -y podman
    apt-get install -y amqp-tools
  SHELL

  if `uname -m`.strip == "aarch64"
    config.vm.box = settings["software"]["box"] + "-arm64"
  else
    config.vm.box = settings["software"]["box"]
  end
  config.vm.box_check_update = true

  if settings["nodes"]["control"]
  config.vm.define "controlplane" do |controlplane|
    controlplane.vm.hostname = "controlplane"
    controlplane.vm.network "private_network", ip: settings["network"]["control_ip"]
    if settings["shared_folders"]
      settings["shared_folders"].each do |shared_folder|
        controlplane.vm.synced_folder shared_folder["host_path"], shared_folder["vm_path"]
      end
    end
    controlplane.vm.provider "virtualbox" do |vb|
        vb.cpus = settings["nodes"]["control"]["cpu"]
        vb.memory = settings["nodes"]["control"]["memory"]
        if settings["cluster_name"] and settings["cluster_name"] != ""
          vb.customize ["modifyvm", :id, "--groups", ("/" + settings["cluster_name"])]
        end
	vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
    end
    controlplane.vm.provision "shell",
      env: {
        "DNS_SERVERS" => settings["network"]["dns_servers"].join(" "),
        "ENVIRONMENT" => settings["environment"],
        "KUBERNETES_VERSION" => settings["software"]["kubernetes"],
        "KUBERNETES_VERSION_SHORT" => settings["software"]["kubernetes"][0..3],
        "OS" => settings["software"]["os"]
      },
      path: "scripts/common.sh"
    controlplane.vm.provision "shell",
      env: {
        "CALICO_VERSION" => settings["software"]["calico"],
        "CONTROL_IP" => settings["network"]["control_ip"],
        "POD_CIDR" => settings["network"]["pod_cidr"],
        "SERVICE_CIDR" => settings["network"]["service_cidr"]
      },
      path: "scripts/master.sh"
    controlplane.vm.provision "shell",
      path: "scripts/helm.sh"
    controlplane.vm.provision "shell",
      path: "scripts/rabbitmq.sh"
    controlplane.vm.provision "shell",
      path: "scripts/wireguard.sh"
    controlplane.vm.provision "file", 
      source: "hooks/50-ifup-hooks", 
      destination: "/tmp/"
    controlplane.vm.provision "shell", inline: <<-SHELL
      cp /tmp/50-ifup-hooks /etc/networkd-dispatcher/routable.d/
      ln -s /etc/networkd-dispatcher/routable.d/50-ifup-hooks /etc/networkd-dispatcher/degraded.d/
    SHELL
  end
  end

  (1..NUM_WORKER_NODES).each do |i|

    config.vm.define "#{WORKER_PREFIX}node0#{i}" do |node|
      node.vm.hostname = "#{WORKER_PREFIX}node0#{i}"
      if WORKER_PREFIX == ""
        node.vm.network "private_network", ip: IP_NW + "#{IP_START + i}"
      end
      if settings["shared_folders"]
        settings["shared_folders"].each do |shared_folder|
          node.vm.synced_folder shared_folder["host_path"], shared_folder["vm_path"]
        end
      end
      node.vm.provider "virtualbox" do |vb|
          vb.cpus = settings["nodes"]["workers"]["cpu"]
          vb.memory = settings["nodes"]["workers"]["memory"]
          if settings["cluster_name"] and settings["cluster_name"] != ""
            vb.customize ["modifyvm", :id, "--groups", ("/" + settings["cluster_name"])]
          end
      end
      node.vm.provision "shell",
        env: {
          "DNS_SERVERS" => settings["network"]["dns_servers"].join(" "),
          "ENVIRONMENT" => settings["environment"],
          "KUBERNETES_VERSION" => settings["software"]["kubernetes"],
          "KUBERNETES_VERSION_SHORT" => settings["software"]["kubernetes"][0..3],
          "OS" => settings["software"]["os"]
        },
        path: "scripts/common.sh"

      node.vm.provision "shell",
        path: "scripts/helm.sh"
      config.vm.provision "shell",
        path: "scripts/wireguard.sh"
      if settings["nodes"]["control"]
      node.vm.provision "shell", path: "scripts/node.sh"

      # Only install the dashboard after provisioning the last worker (and when enabled).
      if i == NUM_WORKER_NODES
        if settings["software"]["dashboard"] and settings["software"]["dashboard"] != ""
          node.vm.provision "shell" do |s|
            s.privileged= false
            s.path= "scripts/dashboard.sh"
          end
        end
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/image_registry.sh"
        end
      end
      end
    end
  end

end 
