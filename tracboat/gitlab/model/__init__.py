# -*- coding: utf-8 -*-

import importlib
import logging

LOG = logging.getLogger(__name__)

def get_model(gitlab_version):
    module_name = 'model' + gitlab_version.replace('.', '').strip()
    module_path = 'tracboat.gitlab.model.' + module_name
    try:
        return importlib.import_module(module_path)
    except ImportError:
        LOG.error('cannot find a database model for GitLab ver. %s', gitlab_version)
        return None
