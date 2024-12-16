#!/bin/bash
#
# Deploys RabbitMQ

set -euxo pipefail

#RABBITMQ_VERSION=$(grep -E '^\s*rabbitmq:' /vagrant/settings.yaml | sed -E -e 's/[^:]+: *//' -e 's/\r$//')
#kubectl apply -f https://github.com/rabbitmq/cluster-operator/releases/download/v${RABBITMQ_VERSION}/cluster-operator.yml

echo "Creating rabbitmq service and statefulset..."
kubectl apply -f /vagrant/rabbitmq-service.yaml
kubectl apply -f /vagrant/rabbitmq-statefulset.yaml
