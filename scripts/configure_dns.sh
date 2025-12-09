#!/bin/bash

set -euxo pipefail

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
FallbackDNS=
Domains=default.svc.cluster.local svc.cluster.local
DNSSEC=no
Cache=no-negative
EOF

sudo systemctl restart systemd-resolved
