#!/bin/bash

set -euxo pipefail

KUBE_STATE_VERSION="5.28.0"

echo "Install Kube-state-metrics ..."

helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

#helm -n loki  upgrade --install --create-namespace loki grafana/loki -f /vagrant/loki_values.yaml
helm -n state upgrade --install --create-namespace kube-state-metrics prometheus-community/kube-state-metrics --version ${KUBE_STATE_VERSION} -f /vagrant/kube-state_values.yaml

#helm upgrade --install kubernetes-dashboard kubernetes-dashboard/kubernetes-dashboard --create-namespace --namespace kubernetes-dashboard --version ${DASHBOARD_VERSION} -f /vagrant/dashboard_values.yaml


# uninstall
# helm -n state uninstall kube-state-metrics
