# -*- coding: utf-8 -*-

import toml

from tracboat.dataloader import DataLoaderInterface


class Toml(DataLoaderInterface):
    def load(self, content):
        return toml.loads(content)

    def dump(self, obj):
        return toml.dumps(obj)
