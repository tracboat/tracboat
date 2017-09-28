#!/bin/sh
set -x

./tracboat.sh -vv --config-file="$@" migrate >out.log 2>error.log || tail error.log 
