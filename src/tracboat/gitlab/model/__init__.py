# -*- coding: utf-8 -*-

import importlib
import logging

__all__ = ['get_model']

__here__ = __name__

LOG = logging.getLogger(__here__)

def get_model(gitlab_version):
    module_name = 'model' + gitlab_version.replace('.', '').strip()
    module_path = __here__ + '.' + module_name
    try:
        return importlib.import_module(module_path)
    except ImportError:
        LOG.error('cannot find a database model for GitLab ver. %s', gitlab_version)
        raise
