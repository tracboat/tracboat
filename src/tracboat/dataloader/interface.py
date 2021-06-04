# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod


class DataLoaderInterface:
    __metaclass__ = ABCMeta

    @classmethod
    def version(self): return "1.0"

    @abstractmethod
    def load(self, content):
        raise NotImplementedError

    @abstractmethod
    def dump(self, obj):
        raise NotImplementedError
