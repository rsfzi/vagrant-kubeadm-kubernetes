#!/bin/bash

HOST=se-ginkgo

PORTS=(6443 32000 32001 30300 30500)
#PORTS+=(8080)
FORWARDS=""

for port in "${PORTS[@]}"
do
    FORWARDS+=" -L ${port}:10.0.0.10:${port}"
done
#echo $FORWARDS

ssh $HOST $FORWARDS
