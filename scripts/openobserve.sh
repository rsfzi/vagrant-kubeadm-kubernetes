#!/bin/bash

set -euxo pipefail

echo "Install OpenObserve..."

kubectl apply -f /vagrant/openobserve-namespace.yaml
kubectl apply -f /vagrant/openobserve-pvc.yaml
kubectl apply -f /vagrant/openobserve-pv.yaml
kubectl apply -f /vagrant/openobserve-statefulset.yaml
