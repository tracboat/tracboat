#!/bin/sh
set -xe

./env.sh

package='gitlab-ce'
version=$(dpkg-query -f '${Version}\n' -W "$package")
ver=$(echo "$version" | cut -d. -f1,2 | tr -d .)

model=src/tracboat/gitlab/model/model$ver.py
sudo -H -u git VENV/bin/pwiz.py -u gitlab --engine=postgresql --host=/var/opt/gitlab/postgresql gitlabhq_production > $model
chmod a+r $model
git add $model
git commit -m "add model for $version" $model
