#!/bin/bash

appname=$1

kubectl get services -n default | grep -e $appname -e CLUSTER-IP
