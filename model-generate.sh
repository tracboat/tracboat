#!/bin/sh
set -xe

./env.sh

package='gitlab-ce'
version=$(dpkg-query -f '${Version}\n' -W "$package")
ver=$(echo "$version" | cut -d. -f1,2 | tr -d .)

model=src/tracboat/gitlab/model/model$ver.py
sudo -H -u git VENV/bin/pwiz.py -u gitlab --engine=postgresql --host=/var/opt/gitlab/postgresql gitlabhq_production > $model

patch -R $model <<EOF
--- src/tracboat/gitlab/model/model104.py	2018-01-02 20:52:44.144989068 +0200
+++ src/tracboat/gitlab/model/model104.py	2018-02-07 13:29:43.314348521 +0200
@@ -1,15 +1,13 @@
-# -*- coding: utf-8 -*-
-
 from peewee import *
 
-database_proxy = Proxy()
+database = PostgresqlDatabase('gitlabhq_production', **{'host': '/var/opt/gitlab/postgresql', 'user': 'gitlab'})
 
 class UnknownField(object):
-    pass
+    def __init__(self, *_, **__): pass
 
 class BaseModel(Model):
     class Meta:
-        database = database_proxy
+        database = database
 
 class AbuseReports(BaseModel):
     cached_markdown_version = IntegerField(null=True)
EOF

chmod a+r $model
git add $model
git commit -m "add model for $version" $model
