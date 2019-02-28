# -*- coding: utf-8 -*-
import pickle

from tracboat.dataloader import DataLoaderInterface


class Pickle(DataLoaderInterface):
    def load(self, content):
        return pickle.loads(content)

    def dump(self, obj):
        return pickle.dumps(obj)
