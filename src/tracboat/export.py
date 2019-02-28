# -*- coding: utf-8 -*-

import codecs
import json
import pickle
import pprint
import toml
from bson import json_util

from tracboat import trac


class Exporter():
    def __init__(self, trac, logger):
        self.trac = trac
        self.logger = logger

    def export_file(self, out_file, format):
        with codecs.open(out_file, 'wb', encoding='utf-8') as f:
            f.write(self.export(format))

    def export_stream(self, stream, format):
        stream.echo(self.export(format))

    def export(self, format):
        data = trac.project_get(self.trac, collect_authors=True)
        return self._dumps(data, format)

    def _dumps(obj, format=None):
        if format == 'toml':
            return toml.dumps(obj)
        elif format == 'json':
            return json.dumps(obj, sort_keys=True, indent=2, default=json_util.default)
        elif format == 'python':
            return pprint.pformat(obj, indent=2)
        elif format == 'pickle':
            return pickle.dumps(obj)
        else:
            return str(obj)
