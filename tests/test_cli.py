# -*- coding: utf-8 -*-
import os

import pytest
import click
from click.testing import CliRunner

from tracboat import cli

__here__ = os.path.abspath(os.path.dirname(__file__))

@pytest.mark.parametrize('export_file,users', [
    [os.path.join(__here__, 'trac-exampleproject-exported.json'), ['userfoo', 'userbar']],
])
def test_users(export_file, users):
    runner = CliRunner()
    result = runner.invoke(cli.users, catch_exceptions=False, args=['--from-export-file', export_file])
    assert result.exit_code == 0
    assert result.output in {"['userfoo', 'userbar']\n", "[u'userfoo', u'userbar']\n"}


@pytest.mark.parametrize('export_file', [
    os.path.join(__here__, 'trac-exampleproject-exported.json'),
])
def test_migrate(export_file, tmpdir):
    runner = CliRunner()
    result = runner.invoke(cli.migrate, obj={}, catch_exceptions=False, args=['--from-export-file', export_file, '--mock', '--mock-path', str(tmpdir)])
    assert result.exit_code == 0
