#!/bin/bash

set -euxo pipefail

systemctl stop kubelet
systemctl stop cri-o
poweroff
