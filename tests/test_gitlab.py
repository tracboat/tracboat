# -*- coding: utf-8 -*-

import pytest

from tracboat import gitlab

@pytest.mark.parametrize('project_name,exp_project,exp_components', [
    ['/ Project ',              'Project',  []],
    ['G1/G2/Pro\ject',          'Pro\ject', ['G1', 'G2']],
    [' Pro ject ',              'Pro ject', []],
    [' G 1/   G 2   /Pro ject', 'Pro ject', ['G 1', 'G 2']],
])
def test_get_project_components(project_name, exp_project, exp_components):
    project, components = gitlab.get_project_components(project_name)
    assert project == exp_project
    assert components == exp_components
