#!/bin/bash

set -euxo pipefail

echo "Install kafka..."
# based on:
# https://dev.to/ciscoemerge/deploy-apache-kafkar-on-kubernetes-5257
kubectl apply -f /vagrant/kafka-namespace.yaml 
kubectl apply -f /vagrant/kafka-network.yaml 
kubectl apply -f /vagrant/kafka-zookeeper.yaml 
kubectl apply -f /vagrant/kafka-broker.yaml 

#kubectl create namespace kafka
#kubectl create -f 'https://strimzi.io/install/latest?namespace=kafka' -n kafka
##kubectl apply -f https://strimzi.io/examples/latest/kafka/kraft/kafka-single-node.yaml -n kafka
#kubectl apply -f /vagrant/kafka-single-node.yaml -n kafka

#kubectl apply -f /vagrant/kafka-ui.yaml
