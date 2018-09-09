#!/bin/sh
set -e

. VENV/bin/activate
tracboat=$(which tracboat)

sudo -H -u git "$tracboat" "$@"
