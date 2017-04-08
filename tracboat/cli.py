# -*- coding: utf-8 -*-

import os
import ast
import errno
import pickle
import functools
import logging
from os import path
from pprint import pformat
from six.moves.urllib import parse as urllib

import six
import click
import toml
import json
import peewee
from bson import json_util

from . import migrate as trac_migrate
from . import trac
from . import VERSION


CONTEXT_SETTINGS = {
    'max_content_width': 120,
    'auto_envvar_prefix': 'TRACBOAT',
    'default_map': {},
}

################################################################################
# utils
################################################################################

def _dumps(obj, format=None):
    if format == 'toml':
        return toml.dumps(obj)
    elif format == 'json':
        return json.dumps(obj, sort_keys=True, indent=2, default=json_util.default)
    elif format == 'python':
        return pformat(obj, indent=2)
    elif format == 'pickle':
        return pickle.dumps(obj)
    else:
        return str(obj)


def _detect_format(filename):
    _, ext = path.splitext(filename)
    ext = ext.strip().strip('.')
    if ext == 'toml':
        return ext
    elif ext in ['json', 'bson']:
        return ext
    elif ext in ['py', 'python', 'pyc']:
        return 'python'
    elif ext in ['pickle']:
        return 'pickle'


def _loads(content, format=None):
    if format == 'toml':
        return toml.loads(content)
    elif format == 'json':
        return json.loads(content, object_hook=json_util.object_hook)
    elif format == 'python':
        return ast.literal_eval(content)
    elif format == 'pickle':
        return pickle.loads(content)
    else:
        return content


def _mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def sanitize_url(url):
    """Strip out username and password if included in URL"""
    if '@' in url:
        parts = urllib.urlparse(url)
        hostname = parts.hostname
        if parts.port:
            hostname += ":%s" % parts.port
        url = urllib.urlunparse((parts.scheme, hostname, parts.path,
                          parts.params, parts.query, parts.fragment))
    return url

################################################################################
# common parameter groups
################################################################################

def TRAC_OPTIONS(func):
    @click.option(
        '--trac-uri',
        metavar='<uri>',
        default='http://localhost/xmlrpc',
        show_default=True,
        help='uri of the Trac instance XMLRpc endpoint',
    )
    @click.option(
        '--ssl-verify / --no-ssl-verify',
        default=True,
        show_default=True,
        help='Enable/disable SSL certificate verification'
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


def GITLAB_OPTIONS(func):
    @click.option(
        '--gitlab-project-name',
        metavar='<str>',
        default='migrated/trac-project',
        show_default=True,
        help='GitLab destination project name',
    )
    @click.option(
        '--gitlab-db-user',
        metavar='<str>',
        default='gitlab',
        show_default=True,
        help='GitLab database username',
    )
    @click.option(
        '--gitlab-db-password',
        metavar='<str>',
        help='GitLab database password',
    )
    @click.option(
        '--gitlab-db-name',
        metavar='<str>',
        default='gitlabhq_production',
        show_default=True,
        help='GitLab database schema name',
    )
    @click.option(
        '--gitlab-db-path',
        metavar='<path>',
        type=click.Path(),
        default='/var/opt/gitlab/postgresql/',
        show_default=True,
        help='GitLab database path',
    )
    @click.option(
        '--gitlab-uploads-path',
        metavar='<path>',
        type=click.Path(),
        default='/var/opt/gitlab/gitlab-rails/uploads',
        show_default=True,
        help='GitLab uploads storage directory path',
    )
    @click.option(
        '--gitlab-version',
        metavar='<str>',
        default='9.0.0',
        show_default=True,
        help='GitLab target version',
    )
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


################################################################################
# main command group
################################################################################

@click.group(context_settings=CONTEXT_SETTINGS)
@click.option(
    '--config-file',
    metavar='<path>',
    type=click.Path(exists=True, readable=True),
    help='Configuration file to be read for options (in toml format). '
         'Values in this file will be overridden by command line/env var values'
)
@click.option(
    '-v', '--verbose',
    count=True,
    help='Run in verbose mode'
)
@click.version_option(VERSION)
@click.pass_context
def cli(ctx, config_file, verbose):
    """Toolbox for Trac to GitLab migrations."""
    # Read config file and update context_map
    if config_file:
        conf = toml.load(config_file).get('tracboat', {})
        ctx.default_map.update(
            {k: conf for k in ['users', 'migrate', 'export']})
    # Convert verbosity to logging levels
    if verbose == 1:
        level = logging.INFO
    elif verbose >= 2:
        level = logging.DEBUG
    else:  # < 1
        level = logging.ERROR
    logging.basicConfig(level=level, format='%(levelname)-5s %(name)s: %(message)s')
    # Pass configuration to subcommands
    ctx.obj['verbose'] = verbose
    ctx.obj['config-file'] = config_file


################################################################################
# subcommands
################################################################################

@cli.command()
@TRAC_OPTIONS
@click.option(
    '--from-export-file',
    metavar='<path>',
    type=click.Path(exists=True, readable=True),
    help="Don't retrieve Trac project from an instance, read it from a "
         "previously exported file instead; the file format will be guessed "
         "from extension and content."
)
@click.pass_context
def users(ctx, trac_uri, ssl_verify, from_export_file):
    """collect users from a Trac instance"""
    LOG = logging.getLogger(ctx.info_name)
    #
    if from_export_file:
        LOG.info('loading Trac instance from export file: %s', from_export_file)
        fmt = _detect_format(from_export_file)
        LOG.debug('detected file format: %s', fmt)
        with open(from_export_file, 'r') as f:
            content = f.read()
        project = _loads(content, format=fmt)
        authors = project['authors']
    else:
        LOG.info('crawling Trac instance: %s', sanitize_url(trac_uri))
        source = trac.connect(trac_uri, encoding='UTF-8', use_datetime=True,
                              ssl_verify=ssl_verify)
        authors = trac.authors_get(source)
    #
    LOG.info('done collecting Trac users')
    click.echo(pformat(authors, indent=2))


@cli.command()
@TRAC_OPTIONS
@click.option(
    '--format',
    type=click.Choice(['json', 'python', 'pickle']),
    default='pickle',
    show_default=True,
    help='export format',
)
@click.option(
    '--out-file',
    metavar='<path>',
    type=click.Path(writable=True),
    help='Output file. If not specified, result will be written to stdout.'
)
@click.pass_context
def export(ctx, trac_uri, ssl_verify, format, out_file):
    """export a complete Trac instance"""
    LOG = logging.getLogger(ctx.info_name)
    #
    LOG.info('crawling Trac instance: %s', sanitize_url(trac_uri))
    source = trac.connect(trac_uri, encoding='UTF-8', use_datetime=True,
                            ssl_verify=ssl_verify)
    project = trac.project_get(source, collect_authors=True)
    project = _dumps(project, format=format)
    if out_file:
        LOG.info('writing export to %s', out_file)
        with open(out_file, 'w') as f:
            f.write(project)
    else:
        click.echo(project)


@cli.command()
@click.option(
    '-u', '--usermap',
    type=(six.u, six.u),
    multiple=True,
    help='Mapping from a Trac username to a GitLab username',
)
@click.option(
    '--usermap-file',
    metavar='<path>...',
    type=click.Path(exists=True, readable=True),
    multiple=True,
    help='Additional file to be read for user mappings ([usermap] section in toml format)',
)
@click.option(
    '--fallback-user',
    metavar='<str>',
    default='migration-bot',
    show_default=True,
    help='Default GitLab username to be used when a Trac user has no match in the user map',
)
@click.option(
    '--wiki-path',
    metavar='<path>',
    type=click.Path(),
    default='wiki.export',
    show_default=True,
    help='Destination path for the exported wiki tree.',
)
@click.option(
    '--from-export-file',
    metavar='<path>',
    type=click.Path(exists=True, readable=True),
    help="Don't retrieve Trac project from an instance, read it from a "
         "previously exported file instead; the file format will be guessed "
         "from extension and content."
)
@TRAC_OPTIONS
@GITLAB_OPTIONS
@click.option(
    '--mock',
    is_flag=True,
    default=False,
    show_default=True,
    help="Don't migrate to a real GitLab instance, migrate to a local file "
         "system instead; a SQLite database file will be used to mock the "
         "GitLab database.",
)
@click.option(
    '--mock-path',
    metavar='<path>',
    type=click.Path(),
    default='gitlab-mock-export',
    show_default=True,
    help='Destination path for the mock export.',
)
# @click.confirmation_option(prompt='Are you sure you want to proceed with the migration?')
@click.pass_context
def migrate(ctx, usermap, usermap_file, fallback_user, trac_uri, ssl_verify,
            gitlab_project_name, gitlab_db_user, gitlab_db_password, gitlab_db_name,
            gitlab_db_path, gitlab_uploads_path, gitlab_version, wiki_path,
            from_export_file, mock, mock_path):
    """migrate a Trac instance"""
    LOG = logging.getLogger(ctx.info_name)
    # 0. Build usermap
    umap = {}
    config_file = ctx.obj.get('config-file', None)
    if config_file:
        umap.update(toml.load(config_file)['usermap'])
    for mapfile in usermap_file:
        umap.update(toml.load(mapfile)['usermap'])
    umap.update({m[0]: m[1] for m in usermap})
    # 1. Retrieve trac project
    if from_export_file:
        LOG.info('loading Trac instance from export file: %s', from_export_file)
        fmt = _detect_format(from_export_file)
        LOG.debug('detected file format: %s', fmt)
        with open(from_export_file, 'r') as f:
            content = f.read()
        project = _loads(content, format=fmt)
    else:
        LOG.info('crawling Trac instance: %s', sanitize_url(trac_uri))
        source = trac.connect(trac_uri, encoding='UTF-8', use_datetime=True,
                              ssl_verify=ssl_verify)
        project = trac.project_get(source, collect_authors=True)
    # 2. Connect to database
    if mock:
        LOG.info('migrating Trac project to mock GitLab')
        mock_path = path.abspath(path.join(mock_path, gitlab_project_name))
        db_path = path.join(mock_path, 'gitlab', 'database.sqlite3')
        gitlab_uploads_path = path.join(mock_path, 'gitlab', 'uploads')
        wiki_path = path.join(mock_path, 'wiki')
        _mkdir_p(mock_path)
        _mkdir_p(db_path)
        _mkdir_p(gitlab_uploads_path)
        _mkdir_p(wiki_path)
        db_connector = peewee.SqliteDatabase(path.join(db_path, 'database.sqlite3'))
    else:
        LOG.info('migrating Trac project to GitLab')
        db_connector = \
            peewee.PostgresqlDatabase(gitlab_db_name, user=gitlab_db_user,
                                      password=gitlab_db_password,
                                      host=gitlab_db_path)
    # 3. Migrate
    LOG.debug('Trac: %s', sanitize_url(trac_uri))
    LOG.debug('GitLab project: %s', gitlab_project_name)
    LOG.debug('GitLab version: %s', gitlab_version)
    LOG.debug('GitLab db path: %s', gitlab_db_path)
    LOG.debug('GitLab db name: %s', gitlab_db_name)
    LOG.debug('GitLab uploads: %s', gitlab_uploads_path)
    LOG.debug('GitLab fallback user: %s', fallback_user)
    trac_migrate.migrate(
        trac=project,
        gitlab_project_name=gitlab_project_name,
        gitlab_version=gitlab_version,
        gitlab_db_connector=db_connector,
        output_wiki_path=wiki_path,
        output_uploads_path=gitlab_uploads_path,
        gitlab_fallback_user=fallback_user,
        usermap=umap
    )
    LOG.info('migration done.')

################################################################################
# setuptools entrypoint
################################################################################

def main():
    cli(obj={})
