#!/bin/bash
#
# Setup for Node servers

set -euxo pipefail

mkdir -p /var/lib/registry

config_path="/vagrant/configs"

/bin/bash $config_path/join.sh -v

sudo -i -u vagrant bash << EOF
whoami
mkdir -p /home/vagrant/.kube
sudo cp -i $config_path/config /home/vagrant/.kube/
sudo chown 1000:1000 /home/vagrant/.kube/config
NODENAME=$(hostname -s)
kubectl label node $(hostname -s) node-role.kubernetes.io/worker=worker
EOF

cat << EOF >> /etc/containers/registries.conf
[[registry]]
location = "10.0.0.10:30500"
insecure = true
EOF
systemctl restart crio
