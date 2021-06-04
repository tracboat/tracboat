# -*- coding: utf-8 -*-

import json
from bson import json_util

from tracboat.dataloader import DataLoaderInterface


class Json(DataLoaderInterface):
    def load(self, content):
        return json.loads(content, object_hook=json_util.object_hook)

    def dump(self, obj):
        return json.dumps(obj, sort_keys=True, indent=2, default=json_util.default)
