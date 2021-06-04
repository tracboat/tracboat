# -*- coding: utf-8 -*-
import ast
import pprint

from tracboat.dataloader import DataLoaderInterface


class Python(DataLoaderInterface):
    def load(self, content):
        return ast.literal_eval(content)

    def dump(self, obj):
        return pprint.pformat(obj, indent=2)
