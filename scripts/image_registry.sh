#!/bin/bash

set -euxo pipefail

kubectl apply -f /vagrant/image-registry.yaml

# Wait for pod
while kubectl get pods -A -l app=registry | awk 'split($3, a, "/") && a[1] != a[2] { print $0; }' | grep -v "RESTARTS"; do
    echo 'Waiting for image-registry to be ready...'
    sleep 5
  done
  echo 'image-registry is ready.'

echo 'login to image-registry'
# https://kubernetes.io/docs/tasks/configure-pod-container/pull-image-private-registry/
podman login -u u -p p 10.0.0.10:30500 --tls-verify=false
kubectl create secret generic cred-simexp-registry --from-file=.dockerconfigjson=$XDG_RUNTIME_DIR/containers/auth.json --type=kubernetes.io/dockerconfigjson
#cat $XDG_RUNTIME_DIR/containers/auth.json
podman logout 10.0.0.10:30500

