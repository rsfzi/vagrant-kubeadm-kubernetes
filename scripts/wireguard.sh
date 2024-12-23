#!/bin/bash
#
# Wireguard

set -euxo pipefail

echo "Installing wireguard..."
apt-get install -y wireguard

config_path="/vagrant/configs"

if [ ! -d $config_path ]; then
  mkdir -p $config_path
fi

NODENAME=$(hostname -s)
wg genkey | tee host_$NODENAME.key | wg pubkey > host_$NODENAME.pub
cp host_$NODENAME.pub $config_path/
