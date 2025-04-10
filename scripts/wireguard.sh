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

echo "Copy existing wireguard keys..."
cp -v /vagrant/*.pub $config_path/ 2>/dev/null || :

NODENAME=$(hostname -s)
if [ "${NODENAME}" != "controlplane" ]; then
  if [ ! -f host_$NODENAME.key ]; then
    echo "Create wireguard keys..."
    wg genkey | tee host_$NODENAME.key | wg pubkey > host_$NODENAME.pub
    cp host_$NODENAME.pub $config_path/
  fi
fi
