# -*- coding: utf-8 -*-
import os
import json
import codecs
from collections import OrderedDict

import six
import pytest
import mock
import click
import peewee
from click.testing import CliRunner

from tracboat import migrate
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
    result = runner.invoke(cli.users, catch_exceptions=False,
                           args=['--from-export-file', export_file])
    assert result.exit_code == 0
    assert result.output == str(users) + '\n'


def test_migrate(export_file, tmpdir):
    runner = CliRunner()
    memory_db = peewee.SqliteDatabase(':memory:')
    migrate_mock = mock.MagicMock(spec=migrate.migrate, side_effect=migrate.migrate)
    with mock.patch('tracboat.cli.peewee.SqliteDatabase', lambda uri: memory_db), \
         mock.patch('tracboat.migrate.migrate', migrate_mock):
        result = runner.invoke(
            cli.migrate, obj={}, catch_exceptions=False,
            args=['--from-export-file', export_file, '--mock', '--mock-path', str(tmpdir)]
        )
        migrate_mock.assert_called()
        assert result.exit_code == 0


@pytest.mark.parametrize('umap,expected', [
    [{}, {}],
    [{'u': 'g'}, {'u': 'g'}],
    [{'u' + str(i): 'g' + str(i) for i in range(20)}, {'u' + str(i): 'g' + str(i) for i in range(20)}],
    [OrderedDict([('u', 'g'), ('u', 'gg')]), {'u': 'gg'}],
    [OrderedDict([('u', 'g'), ('u', 'gg'), ('u', 'ggg')]), {'u': 'ggg'}],
    [OrderedDict([('u', 'g'), ('u', 'gg'), ('U', 'g'), ('u', 'ggg')]), {'u': 'ggg', 'U': 'g'}],
    [OrderedDict([('u', 'g'), ('U', 'G'), ('u', 'gg'), ('U', 'GG')]), {'u': 'gg', 'U': 'GG'}],
])
def test_migrate_usermap_cmd(export_file, umap, expected):  # TODO remove the need for an actual export_file
    runner = CliRunner()
    migrate_mock = mock.MagicMock(spec=migrate.migrate)
    with mock.patch('tracboat.migrate.migrate', migrate_mock):
        umap_args = []
        for k, v in six.iteritems(umap):
            umap_args += ['--umap', k, v]
        result = runner.invoke(
            cli.migrate, obj={}, catch_exceptions=False,
            args=['--from-export-file', export_file, '--mock'] + umap_args
        )
        assert result.exit_code == 0
        migrate_mock.assert_called_once()
        args, kwargs = migrate_mock.call_args
        assert 'usermap' in kwargs
        assert kwargs['usermap'] == expected
