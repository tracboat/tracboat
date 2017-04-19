# -*- coding: utf-8 -*-

import pytest

try:
    from unittest.mock import patch
except ImportError:
    from mock import patch

from tracboat.gitlab import *

@pytest.mark.parametrize('project_name,exp_project,exp_components', [
    ['/ Project ',              'Project',  []],
    ['G1/G2/Pro\ject',          'Pro\ject', ['G1', 'G2']],
    [' Pro ject ',              'Pro ject', []],
    [' G 1/   G 2   /Pro ject', 'Pro ject', ['G 1', 'G 2']],
])
def test_get_project_components(project_name, exp_project, exp_components):
    project, components = get_project_components(project_name)
    assert project == exp_project
    assert list(components) == exp_components


def test_connectionbase():
        # Temporarily disable ABC checks
        with patch.multiple(ConnectionBase, __abstractmethods__=set()):
            with pytest.raises(TypeError):
                ConnectionBase()
            c = ConnectionBase('project')
            assert c.project_name == 'project'
            assert not c.project_namespace
            assert c.project_qualname == 'project'
            c = ConnectionBase('ns/project')
            assert c.project_name == 'project'
            assert c.project_namespace == 'ns'
            assert c.project_qualname == 'ns/project'
