#!/bin/bash
#
# Setup for Node remote worker

set -euo pipefail

usage()
{
cat << EOF_HELP
Usage: $(basename $0) -i ip address -g gateway [-p priority]
EOF_HELP
}

ADDRESS=
GATEWAY=
while getopts 'i:g:p:h' opt; do
  case "$opt" in
    i)
      ADDRESS=${OPTARG}
      ;;

    g)
      GATEWAY=${OPTARG}
      ;;

    p)
      export NODE_PRIORITY=${OPTARG}
      ;;

    ?|h)
      usage
      exit 1
      ;;
  esac
done
shift "$(($OPTIND -1))"
if [[ -z $ADDRESS ]] || [[ -z $GATEWAY ]] 
then
     usage
     exit 1
fi


script_path="/vagrant/scripts"
config_path="/vagrant/configs"

PORT=51820

NODENAME="$(tr '[:upper:]' '[:lower:]' <<< $(hostname -s))"
read -r PRIVATE_KEY < host_${NODENAME}.key

read -r GW_PUBLIC_KEY < $config_path/host_controlplane.pub

cat << EOF  > /etc/wireguard/wg0.conf
# local settings 
[Interface]
PrivateKey = $PRIVATE_KEY
Address = $ADDRESS/32
#ListenPort = 51821
#ListenPort = $PORT

# remote GW settings
[Peer]
PublicKey = $GW_PUBLIC_KEY
Endpoint = $GATEWAY:$PORT
AllowedIPs = 10.1.0.1/32,10.0.0.10/32
PersistentKeepalive = 30
EOF

systemctl enable wg-quick@wg0
systemctl restart wg-quick@wg0

cat << EOF  > /etc/default/kubelet
KUBELET_EXTRA_ARGS=--node-ip=$ADDRESS
EOF

/bin/bash $script_path/node.sh

sudo -i -u vagrant bash << EOF
kubectl taint nodes $(hostname -s) remote=true:NoExecute --overwrite=true
EOF

