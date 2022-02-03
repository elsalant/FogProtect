#!/usr/bin/env bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
crdoc --template ./main.tmpl --resources ../manifests --output ../docs/README.md
