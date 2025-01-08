#!/bin/bash

set -euxo pipefail

echo "Install fluentbit logging..."
helm repo add fluent https://fluent.github.io/helm-charts
helm -n fluent upgrade --install --create-namespace fluent-bit fluent/fluent-bit -f /vagrant/fluentbit_values.yaml

# helm -n fluent uninstall fluent-bit
