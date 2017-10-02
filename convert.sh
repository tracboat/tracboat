#!/bin/sh
set -xe

if [ ! -d VENV ]; then
	virtualenv -p python2.7 VENV
	. VENV/bin/activate
	pip install -r requirements/dist.txt
	pip install -e .
	chmod -R a+rX .
fi

./tracboat.sh -vv --config-file="$@" migrate >out.log 2>error.log || tail error.log 
