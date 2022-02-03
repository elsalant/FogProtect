#!/bin/bash

chartpath=$1


if [ -z $chartpath ]; then
	echo "Usage: ./app_package.sh chartpath "
        echo "       chartpath: the path of the helm chart directory, i.e. protegochart/"
	echo ""
	echo "Please run again with the corresponding parameters"

	exit 1
fi

helm package $chartpath
