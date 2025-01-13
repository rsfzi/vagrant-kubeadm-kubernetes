#!/bin/bash

set -euxo pipefail

LOKI_VERSION=2.9.11
LOCAL_FILE=logcli_${LOKI_VERSION}_amd64.deb

echo "Install Loki CLI..."

cd /var/tmp
wget -c https://github.com/grafana/loki/releases/download/v${LOKI_VERSION}/${LOCAL_FILE}
dpkg -i /var/tmp/${LOCAL_FILE}

echo "export LOKI_ADDR=http://10.0.0.10:32031" >> /home/vagrant/.bashrc
