#!/bin/bash

chartname=$1

appname=$2

if [ -z $chartname ] || [ -z $appname ]; then
	echo "Usage: ./app_deploy.sh chartname appname"
        echo "       chartname: the chart name as stored in the catalog, i.e. protegochart"
	echo "       appname: the name of the app to be given when deploying it, i.e. protegoapp"
	echo ""
	echo "Please run again with the corresponding parameters"

	exit 1
fi


rancher apps install $chartname $appname -n default
