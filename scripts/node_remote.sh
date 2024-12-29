#!/bin/bash
#
# Setup for Node remote worker

set -euxo pipefail

script_path="/vagrant/scripts"

/bin/bash $script_path/node.sh

sudo -i -u vagrant bash << EOF
kubectl taint nodes $(hostname -s) remote=true:NoExecute
EOF