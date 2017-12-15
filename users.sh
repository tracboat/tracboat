#!/bin/sh
set -xe

./env.sh

exec ./tracboat.sh -vv --config-file="$@" users
