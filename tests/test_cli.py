# -*- coding: utf-8 -*-
import os
import json
import codecs

import pytest
import mock
import click
import peewee
from click.testing import CliRunner

from tracboat import cli

__here__ = os.path.abspath(os.path.dirname(__file__))

@pytest.fixture(params=[
    os.path.join(__here__, 'trac-exampleproject-exported.json'),
])
def export_file(request):
    return request.param


def test_users(export_file):
    with codecs.open(export_file, encoding='utf-8') as f:
        prj = json.loads(f.read())
    users = prj['authors']
    runner = CliRunner()
    result = runner.invoke(cli.users, catch_exceptions=False, args=['--from-export-file', export_file])
    assert result.exit_code == 0
    assert result.output == str(users) + '\n'


def test_migrate(export_file, tmpdir):
    runner = CliRunner()
    memory_db = peewee.SqliteDatabase(':memory:')
    with mock.patch('tracboat.cli.peewee.SqliteDatabase', lambda uri: memory_db):
        result = runner.invoke(
            cli.migrate, obj={}, catch_exceptions=False,
            args=['--from-export-file', export_file, '--mock', '--mock-path', str(tmpdir)]
        )
    assert result.exit_code == 0


def test_migrate_usermap():
    pass
