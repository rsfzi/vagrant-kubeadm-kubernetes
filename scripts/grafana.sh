#!/bin/bash

set -euxo pipefail

echo "Install Loki ..."
# see https://vadosware.io/post/installing-fluent-bit-and-loki-for-lightweight-logs/
#helm repo add grafana https://grafana.github.io/helm-charts
#helm -n loki install --create-namespace loki grafana/loki -f /vagrant/loki_values.yaml
#helm -n loki upgrade --install --create-namespace loki grafana/loki -f /vagrant/loki_values.yaml

kubectl apply -f /vagrant/grafana-namespace.yaml
kubectl apply -f /vagrant/grafana-pvc.yaml
kubectl apply -f /vagrant/grafana-pv.yaml
kubectl apply -f /vagrant/grafana-deployment.yaml
