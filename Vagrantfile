
require "yaml"
vagrant_root = File.dirname(File.expand_path(__FILE__))
settings = YAML.load_file "#{vagrant_root}/settings.yaml"

IP_SECTIONS = settings["network"]["control_ip"].match(/^([0-9.]+\.)([^.]+)$/)
# First 3 octets including the trailing dot:
IP_NW = IP_SECTIONS.captures[0]
# Last octet excluding all dots:
IP_START = Integer(IP_SECTIONS.captures[1])
NUM_WORKER_NODES = settings["nodes"]["workers"]["count"]
HOST_NAME = "#{`hostname`.strip.downcase}".delete_prefix("se-")
WORKER_PREFIX = ""
if settings["nodes"]["workers"]["prefix"]
  WORKER_PREFIX = settings["nodes"]["workers"]["prefix"]
else
  if not settings["nodes"]["control"]
    WORKER_PREFIX = HOST_NAME + "-"
  end
end
CLUSTER_NAME = ""
if settings["cluster_name"] and settings["cluster_name"] != ""
  CLUSTER_NAME = settings["cluster_name"]
  if not settings["nodes"]["control"]
    CLUSTER_NAME << " - " + HOST_NAME
  end
end

Vagrant.configure("2") do |config|
  config.vm.provision "shell", inline: "timedatectl set-timezone Europe/Berlin"
  config.vm.provision "shell", inline: <<-'SHELL'
    sed -i 's/GRUB_TIMEOUT=0/GRUB_TIMEOUT=3\nGRUB_RECORDFAIL_TIMEOUT=3/' /etc/default/grub
    update-grub
  SHELL
  config.vm.provision "shell", env: { "IP_NW" => IP_NW, "IP_START" => IP_START, "NUM_WORKER_NODES" => NUM_WORKER_NODES, "WORKER_PREFIX" => WORKER_PREFIX }, inline: <<-SHELL
      apt-get update -y
      echo "### kubernetes entries" >> /etc/hosts
      echo "$IP_NW$((IP_START)) controlplane" >> /etc/hosts
      for i in `seq 1 ${NUM_WORKER_NODES}`; do
        echo "$IP_NW$((IP_START+i)) ${WORKER_PREFIX}node0${i}" >> /etc/hosts
      done
  SHELL
  
  config.vm.provision "shell", inline: <<-SHELL
    apt-get install -y podman
    apt-get install -y amqp-tools
    apt-get install -y fish
    apt-get install -y unzip
    apt-get install -y ncdu
  SHELL
  
  config.vm.provision "shell", inline: <<-SHELL
    cp /vagrant/scripts/shutdown_node.sh /home/vagrant
    chmod 744 /home/vagrant/shutdown_node.sh
  SHELL

  config.vm.provision "shell", privileged:false, inline: <<-SHELL
    cp /vagrant/cluster_rsa* /home/vagrant/.ssh/
    chmod 600 /home/vagrant/.ssh/cluster_rsa
  SHELL

  if `uname -m`.strip == "aarch64"
    config.vm.box = settings["software"]["box"] + "-arm64"
  else
    config.vm.box = settings["software"]["box"]
  end
  config.vm.box_check_update = true

  config.vm.provider "virtualbox" do |vb|
    vb.default_nic_type = "virtio"
  end

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
        if CLUSTER_NAME != ""
          vb.customize ["modifyvm", :id, "--groups", ("/" + CLUSTER_NAME)]
        end
        vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
    end
    controlplane.vm.provision "shell" do |s|
      s.privileged= false
      s.inline= "cat /vagrant/cluster_rsa.pub >> ~/.ssh/authorized_keys"
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
        node.vm.provision "file", 
          source: "hooks/50-ifup-hooks", 
          destination: "/tmp/"
        node.vm.provision "shell", inline: <<-SHELL
          cp /tmp/50-ifup-hooks /etc/networkd-dispatcher/routable.d/
          ln -s /etc/networkd-dispatcher/routable.d/50-ifup-hooks /etc/networkd-dispatcher/degraded.d/
        SHELL
      end
      if settings["shared_folders"]
        settings["shared_folders"].each do |shared_folder|
          node.vm.synced_folder shared_folder["host_path"], shared_folder["vm_path"]
        end
      end
      node.vm.provider "virtualbox" do |vb|
          vb.cpus = settings["nodes"]["workers"]["cpu"]
          vb.memory = settings["nodes"]["workers"]["memory"]
          if CLUSTER_NAME != ""
            vb.customize ["modifyvm", :id, "--groups", ("/" + CLUSTER_NAME)]
          end
      end
      node.vm.provision "shell" do |s|
        s.privileged= false
        s.inline= "cat /vagrant/cluster_rsa.pub >> ~/.ssh/authorized_keys"
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
      node.vm.provision "shell",
        path: "scripts/wireguard.sh"
      node.vm.provision "shell", inline: <<-SHELL
          mkdir /var/lib/grafana
          mkdir /etc/grafana
          ln -s /vagrant/grafana /etc/grafana/provisioning
          mkdir /var/lib/openobserve
      SHELL
      if settings["nodes"]["control"]
        node.vm.provision "shell",
          env: {
            "NODE_PRIORITY" => "5"
          },
          path: "scripts/node.sh"

      if i == 1
        node.vm.provision "shell", privileged: false, inline: <<-SHELL
          kubectl taint nodes node01 datanode=true:NoExecute --overwrite
        SHELL
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/rabbitmq.sh"
        end
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/openobserve.sh"
        end
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/fluentbit.sh"
        end
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/kube-state-metrics.sh"
        end
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/prometheus.sh"
        end
        node.vm.provision "shell" do |s|
          s.privileged= false
          s.path= "scripts/grafana.sh"
        end
      end

      # Only install the dashboard after provisioning the last worker (and when enabled).
      if i == NUM_WORKER_NODES
        if settings["software"]["dashboard"] and settings["software"]["dashboard"] != ""
          node.vm.provision "shell" do |s|
            s.privileged= false
            s.path= "scripts/dashboard.sh"
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

end 
