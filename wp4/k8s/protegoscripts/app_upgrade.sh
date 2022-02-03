#!/bin/bash

appname=$1

version=$2

if [ -z $appname ] || [ -z $version ]; then
	echo "Usage: ./app_upgrade.sh appname version"
	echo "       appname: the name of the app deployed app, i.e. protegoapp"
	echo "       version: the new version of the app to deploy"
	echo ""
	echo "Please run again with the corresponding parameters"

	exit 1
fi


rancher apps upgrade $appname $version
