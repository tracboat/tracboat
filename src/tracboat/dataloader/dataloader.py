# -*- coding: utf-8 -*-
import codecs

from tracboat import trac
from tracboat.dataloader import DataLoaderInterface
from tracboat.dataloader.format import Json, Pickle, Python, Toml


class DataLoader(DataLoaderInterface):
    FORMATS = {
        'json': Json,
        'pickle': Pickle,
        'python': Python,
        'toml': Toml,
    }

    def __init__(self, trac, format, logger):
        self.logger = logger
        self.loader = self.get_loader(format)
        self.trac = trac

    def get_loader(self, format):
        if not format in self.FORMATS:
            raise Exception('Unsupported format: %s' % format)

        loader = self.FORMATS[format]()
        if not isinstance(loader, DataLoaderInterface): raise Exception('Bad interface')
        if not DataLoaderInterface.version() == '1.0': raise Exception('Bad revision')

        return loader

    def load(self, content):
        return self.loader.load(content)

    def dump(self):
        obj = trac.project_get(self.trac, collect_authors=True)
        return self.loader.dump(obj)

    def write_file(self, filename):
        with codecs.open(filename, 'wb', encoding='utf-8') as f:
            f.write(self.dump())
