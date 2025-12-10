#!/bin/bash

set -euxo pipefail

SYSTEM_DNS_FILE=/etc/systemd/resolved.conf.d/dns_servers.conf
if [ ! -e "$SYSTEM_DNS_FILE" ]; then
    echo "system DNS file not found -> skip configuration"!
    exit 0
fi

FALLBACK_DNS="$(grep -m1 '^DNS=' $SYSTEM_DNS_FILE | cut -d'=' -f2-)"

until kubectl get service -n kube-system kube-dns --no_headers -o custom-columns=NAME:.spec.clusterIP; do
    echo 'Waiting for kube-dns  to be ready...'
    sleep 5
  done
echo 'kube-dns is ready.'

COREDNS_IP=$(kubectl get service -n kube-system kube-dns --no_headers -o custom-columns=NAME:.spec.clusterIP)
echo "COREDNS IP: $COREDNS_IP"
cat <<EOF | sudo tee /etc/systemd/resolved.conf.d/kubernetes.conf
[Resolve]
DNS=$COREDNS_IP
FallbackDNS=$FALLBACK_DNS
Domains=default.svc.cluster.local svc.cluster.local
DNSSEC=no
Cache=no-negative
EOF

sudo mv $SYSTEM_DNS_FILE ${SYSTEM_DNS_FILE}_

sudo systemctl restart systemd-resolved
