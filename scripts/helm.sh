#!/bin/bash

set -euxo pipefail

#if [ ! -f "/etc/apt/keyrings/helm.gpg" ]; then
#  curl -fsSL https://baltocdn.com/helm/signing.asc | gpg --dearmor -o /etc/apt/keyrings/helm.gpg
#  chmod 644 /etc/apt/keyrings/helm.gpg
#fi
#if [ ! -f "/etc/apt/sources.list.d/helm-stable.list" ]; then
#  #echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main"| tee /etc/apt/sources.list.d/helm-stable.list
#  echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main"| tee /etc/apt/sources.list.d/helm-stable.list
#  chmod 644 /etc/apt/sources.list.d/helm-stable.list
#fi

#sudo apt-get update -y
#sudo apt-get install -y helm


HELM_VERSION=3.18.6
HELM_ARCHIVE=helm-v$HELM_VERSION-linux-amd64.tar.gz
cd /var/tmp
wget https://get.helm.sh/$HELM_ARCHIVE
tar -zxvf $HELM_ARCHIVE
mkdir -p /usr/local/bin
cp linux-amd64/helm /usr/local/bin
