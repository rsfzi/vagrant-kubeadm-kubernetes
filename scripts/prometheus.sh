#!/bin/bash

set -euxo pipefail

echo "Install Prometheus..."
# see https://heiioncall.com/guides/minimalistic-monitoring-and-alerting-for-your-kubernetes-cluster-with-prometheus-and-alertmanager

kubectl apply -f /vagrant/prometheus-namespace.yaml
kubectl apply -f /vagrant/prometheus-configmap.yaml
#kubectl apply -f /vagrant/grafana-pvc.yaml
#kubectl apply -f /vagrant/grafana-pv.yaml
kubectl apply -f /vagrant/prometheus-deployment.yaml
