#!/bin/sh
set -xe

./env.sh

package='gitlab-ce'
version=$(dpkg-query -f '${Version}\n' -W "$package")
ver=$(echo "$version" | cut -d. -f1,2 | tr -d .)

model=src/tracboat/gitlab/model/model$ver.py
sudo -H -u git VENV/bin/pwiz.py -u gitlab --engine=postgresql --host=/var/opt/gitlab/postgresql gitlabhq_production > $model

patch -p1 $model <<EOF
--- tracboat/src/tracboat/gitlab/model/model1110.py~	2019-04-29 18:09:04.610256015 +0300
+++ tracboat/src/tracboat/gitlab/model/model1110.py	2019-04-29 18:09:47.605995257 +0300
@@ -1,14 +1,16 @@
+# -*- coding: utf-8 -*-
+
 from peewee import *
 from playhouse.postgres_ext import *
 
-database = PostgresqlDatabase('gitlabhq_production', **{'host': '/var/opt/gitlab/postgresql', 'user': 'gitlab'})
+database_proxy = Proxy()
 
 class UnknownField(object):
-    def __init__(self, *_, **__): pass
+    pass
 
 class BaseModel(Model):
     class Meta:
-        database = database
+        database = database_proxy
 
 class AbuseReports(BaseModel):
     cached_markdown_version = IntegerField(null=True)
EOF

chmod a+r $model
git add $model
git commit -m "add model for $version" $model
