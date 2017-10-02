#!/bin/sh
set -xe

. VENV/bin/activate
tracboat=$(which tracboat)

sudo -H -u git "$tracboat" "$@"
