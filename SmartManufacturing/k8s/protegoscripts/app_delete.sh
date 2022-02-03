#!/bin/bash

appname=$1

if [ -z $appname ]; then
	echo "Usage: ./app_delete.sh appname"
	echo "       appname: the name of the app that was given when deploying it, i.e. protegoapp"
	echo ""
	echo "Please run again with the corresponding parameters"

	exit 1
fi


rancher apps delete $appname
