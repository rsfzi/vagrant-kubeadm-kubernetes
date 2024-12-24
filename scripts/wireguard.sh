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
cp -v /vagrant/*.pub $config_path/

NODENAME=$(hostname -s)
if [ ! -f host_$NODENAME.key ]; then
  echo "Create wireguard keys..."
  wg genkey | tee host_$NODENAME.key | wg pubkey > host_$NODENAME.pub
  cp host_$NODENAME.pub $config_path/
fi

if [ -f $config_path/host_gw.pub ]; then
  echo "Prepare wireguard config"
  WG_NODE_IP=10.0.0.10
  PRIVATE_KEY=$(head -n 1 host_$NODENAME.key)
  GW_KEY=$(head -n 1 $config_path/host_gw.pub)

  cat >/etc/wireguard/wg0.conf <<EOF
# local settings
[Interface]
PrivateKey = ${PRIVATE_KEY}
Address = ${WG_NODE_IP}/32
ListenPort = 51821

# remote settings for Hub
[Peer]
PublicKey = ${GW_KEY}
Endpoint = 141.21.51.14:51823
AllowedIPs = 10.1.0.0/24
PersistentKeepalive = 30
EOF
fi
