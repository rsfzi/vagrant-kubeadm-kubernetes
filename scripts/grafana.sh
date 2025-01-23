#!/bin/bash

set -euxo pipefail

echo "Install Grafana ..."

kubectl apply -f /vagrant/grafana-namespace.yaml
kubectl apply -f /vagrant/grafana-pvc.yaml
kubectl apply -f /vagrant/grafana-pv.yaml
kubectl apply -f /vagrant/grafana-deployment.yaml

# see: https://grafana.com/blog/2024/05/30/how-to-export-any-grafana-visualization-to-a-csv-file-microsoft-excel-or-google-sheets/
