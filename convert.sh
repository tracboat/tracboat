#!/bin/sh
set -xe

./env.sh

set +e
./tracboat.sh -vv --config-file="$@" migrate >out.log 2>error.log
tail error.log
