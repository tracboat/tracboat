#!/bin/sh

set -e

if [ ! -d VENV ]; then
	virtualenv -p python2.7 VENV
	. VENV/bin/activate
	pip install -r requirements/dist.txt
	pip install -e .
	chmod -R a+rX .
fi

