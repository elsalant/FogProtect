#!/bin/bash

chartpackage=$1


if [ -z $chartpackage ]; then
	echo "Usage: ./app_catalog.sh chartpackage"
        echo "       chartpackage: the path of the helm chart package, i.e. protegochart-0.1.0.tgz"
	echo ""
	echo "Please run again with the corresponding parameters"

	exit 1
fi


curl --data-binary "@$chartpackage" http://192.168.56.4:30408/api/charts

