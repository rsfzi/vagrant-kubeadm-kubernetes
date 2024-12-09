#!/bin/bash

set -euxo pipefail

if [ ! -f "/etc/apt/keyrings/helm.gpg" ]; then
  curl -fsSL https://baltocdn.com/helm/signing.asc | gpg --dearmor -o /etc/apt/keyrings/helm.gpg
  chmod 644 /etc/apt/keyrings/helm.gpg
fi
if [ ! -f "/etc/apt/sources.list.d/helm-stable.list" ]; then
  #echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main"| tee /etc/apt/sources.list.d/helm-stable.list
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main"| tee /etc/apt/sources.list.d/helm-stable.list
  chmod 644 /etc/apt/sources.list.d/helm-stable.list
fi

sudo apt-get update -y
sudo apt-get install -y helm
