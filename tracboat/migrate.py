# -*- coding: utf-8 -*-

import os
import re
import random
import string
import logging

import six

from tracboat import trac2down
from tracboat.gitlab import model
from tracboat.gitlab import direct

__all__ = ['migrate']

LOG = logging.getLogger(__name__)


TICKET_PRIORITY_TO_ISSUE_LABEL = {
    'high': 'prio:high',
    # 'medium': None,
    'low': 'prio:low',
}

TICKET_RESOLUTION_TO_ISSUE_LABEL = {
    # 'fixed': None,
    'invalid': 'closed:invalid',
    'wontfix': 'closed:wontfix',
    'duplicate': 'closed:duplicate',
    'worksforme': 'closed:worksforme',
}

TICKET_STATE_TO_ISSUE_STATE = {
    'new': 'opened',
    'assigned': 'opened',
    'reopened': 'reopened',
    'closed': 'closed',
}

################################################################################
# Wiki format normalization
################################################################################

_pattern_changeset = r'(?sm)In \[changeset:"([^"/]+?)(?:/[^"]+)?"\]:\n\{\{\{(\n#![^\n]+)?\n(.*?)\n\}\}\}'
_matcher_changeset = re.compile(_pattern_changeset)

_pattern_changeset2 = r'\[changeset:([a-zA-Z0-9]+)\]'
_matcher_changeset2 = re.compile(_pattern_changeset2)


def _format_changeset_comment(m):
    return 'In changeset ' + m.group(1) + ':\n> ' + m.group(3).replace('\n', '\n> ')


def _wikifix(text):
    text = _matcher_changeset.sub(_format_changeset_comment, text)
    text = _matcher_changeset2.sub(r'\1', text)
    return text


def _wikiconvert(text, basepath, multiline=True):
    return trac2down.convert(_wikifix(text), basepath, multiline)

################################################################################
# Trac ticket metadata conversion
################################################################################

def ticket_priority(ticket, priority_to_label=TICKET_PRIORITY_TO_ISSUE_LABEL):
    priority = ticket['attributes']['priority']
    if priority in priority_to_label:
        return {priority_to_label[priority]}
    else:
        return set()


def ticket_resolution(ticket, resolution_to_label=TICKET_RESOLUTION_TO_ISSUE_LABEL):
    resolution = ticket['attributes']['resolution']
    if resolution in resolution_to_label:
        return {resolution_to_label[resolution]}
    else:
        return set()


def ticket_version(ticket):
    version = ticket['attributes']['version']
    if version:
        return {'ver:{}'.format(version)}
    else:
        return set()


def ticket_components(ticket):
    components = ticket['attributes']['component'].split(',')
    return {'comp:{}'.format(comp.strip()) for comp in components}


def ticket_type(ticket):
    type = ticket['attributes']['type']
    return {'type:{}'.format(type.strip())}


def ticket_state(ticket, status_to_state=TICKET_STATE_TO_ISSUE_STATE):
    state = ticket['attributes']['status']
    if state in status_to_state:
        return status_to_state[state], None
    else:
        return None, {'state:{}'.format(state)}

################################################################################
# Trac dict -> GitLab dict conversion
# The GitLab dict is a GitLab model-friendly representation, the GitLab dict
# can be unrolled as kwargs to the corresponding database model entity
# e.g.:
#  dbmodel.Milestone(**milestone_kwargs(trac_milestone))
################################################################################

def change_kwargs(change):
    return {
        'note': _wikiconvert(change['newvalue'], '/issues/', multiline=False),
        'created_at': change['time'],
        'updated_at': change['time'],
        # References:
        'author': change['author'],
        'updated_by': change['author'],
        # 'project'
    }


def ticket_kwargs(ticket):
    priority_labels = ticket_priority(ticket)
    resolution_labels = ticket_resolution(ticket)
    version_labels = ticket_version(ticket)
    component_labels = ticket_components(ticket)
    type_labels = ticket_type(ticket)
    state, state_labels = ticket_state(ticket)

    labels = priority_labels | resolution_labels | version_labels | \
             component_labels | type_labels | state_labels

    return {
        'title': ticket['attributes']['summary'],
        'description': _wikiconvert(ticket['attributes']['description'], '/issues/', multiline=False),
        'state': state,
        'labels': ','.join(labels),
        'created_at': ticket['attributes']['time'],
        'updated_at': ticket['attributes']['changetime'],
        # References:
        'assignee': ticket['attributes']['owner'],
        'author': ticket['attributes']['reporter'],
        'milestone': ticket['attributes']['milestone'],
        # 'project': None,
        # 'iid': None,
    }


def milestone_kwargs(milestone):
    return {
        'description': _wikiconvert(milestone['description'], '/milestones/', multiline=False),
        'title': milestone['name'],
        'state': 'closed' if milestone['completed'] else 'active',
        'due_date': milestone['due'],
        # References:
        # 'project': None,
    }


################################################################################
# Conversion API
################################################################################

def migrate_tickets(trac_tickets, gitlab, default_user, usermap=None):
    for ticket_id, ticket in six.iteritems(trac_tickets):
        issue_args = ticket_kwargs(ticket)
        # Fix references
        issue_args['project'] = gitlab.project_id
        issue_args['milestone'] = gitlab.get_milestone_id(issue_args['milestone'])
        issue_args['author'] = gitlab.get_user_id(username=usermap.get(issue_args['author'], default_user))
        issue_args['assignee'] = gitlab.get_user_id(username=usermap.get(issue_args['assignee'], default_user))
        # Create and save
        gitlab_issue = gitlab.model.Issues(**issue_args)
        db_issue = gitlab.create_issue(gitlab_issue)
        LOG.debug('migrated ticket %s -> %s', ticket_id, db_issue.iid)
        # Migrate whole changelog
        for change in ticket['changelog']:
            if change['field'] == 'comment':
                note_args = change_kwargs(change)
                # Fix references
                note_args['project'] = issue_args['project']
                note_args['author'] = gitlab.get_user_id(username=usermap.get(note_args['author'], default_user))
                note_args['updated_by'] = gitlab.get_user_id(username=usermap.get(note_args['updated_by'], default_user))
                db_note = gitlab.model.Notes(**note_args)
                gitlab.comment_issue(db_issue, db_note, binary_attachment)
                LOG.debug('migrated ticket #%s change -> %s', ticket_id, db_note.iid)


def migrate_milestones(trac_milestones, gitlab):
    for title, milestone in six.iteritems(trac_milestones):
        gitlab_milestone = gitlab.model.Milestones(
            project=gitlab.project_id,
            **milestone_kwargs(milestone)
        )
        db_milestone = gitlab.create_milestone(gitlab_milestone)
        LOG.debug('migrated milestone %s -> %s', title, db_milestone.iid)


def migrate_wiki(trac_wiki, gitlab, output_dir):
    for title, wiki in six.iteritems(trac_wiki):
        page = wiki['page']
        attachments = wiki['attachments']
        author = wiki['attributes']['author']
        version = wiki['attributes']['version']
        last_modified = wiki['attributes']['lastModified']
        if title == 'WikiStart':
            title = 'home'
        converted_page = trac2down.convert(page, os.path.dirname('/wikis/%s' % title))
        orphaned = []
        for filename, data in six.iteritems(attachments):
            name = filename.split('/')[-1]
            gitlab.save_wiki_attachment(name, data)
            converted_page = \
                converted_page.replace(r'migrated/%s)' % filename,
                                       r'migrated/%s)' % name)
            if '%s)' % name not in converted_page:
                orphaned.append(name)
            LOG.debug('migrated attachment %s @ %s', title, filename)
        # Add orphaned attachments to page
        if orphaned:
            converted_page += '\n\n'
            converted_page += '##### During migration the following orphaned attachments have been found:\n'
            for f in orphaned:
                converted_page += '- [%s](/uploads/migrated/%s)\n' % (f, f)
        # Writeout!
        trac2down.save_file(converted_page, title, version, last_modified, author, output_dir)
        LOG.debug('migrated wiki page %s', title)


def generate_password(length=None):
    alphabet = string.letters + string.digits + string.punctuation
    return ''.join(random.choice(alphabet) for _ in range(length or 30))


def migrate(trac, gitlab_project_name, gitlab_version, gitlab_db_connector,
            output_wiki_path, output_uploads_path, gitlab_fallback_user, usermap=None):
    LOG.info('migrating project %s to GitLab ver. %s', gitlab_project_name, gitlab_version)
    LOG.info('uploads repository path is: %s', output_uploads_path)
    db_model = model.get_model(gitlab_version)
    LOG.info('retrieved database model for GitLab ver. %s: %s', gitlab_version, db_model.__file__)
    gitlab = direct.Connection(gitlab_project_name, db_model, gitlab_db_connector, output_uploads_path, create_missing=True)
    LOG.info('estabilished connection to GitLab database')
    # 0. Fallback user
    # TODO allow to specify email
    gitlab.create_user(email=gitlab_fallback_user+'@gmail.com', username=gitlab_fallback_user, encrypted_password=generate_password())
    LOG.info('created fallback GitLab user %r', gitlab_fallback_user)
    # 1. Wiki
    LOG.info('migrating %d wiki pages to: %s', len(trac['wiki']), output_wiki_path)
    migrate_wiki(trac['wiki'], gitlab, output_wiki_path)
    # 2. Milestones
    LOG.info('migrating %d milestones', len(trac['milestones']))
    migrate_milestones(trac['milestones'], gitlab)
    # 3. Issues
    LOG.info('migrating %d tickets to issues', len(trac['tickets']))
    migrate_tickets(trac['tickets'], gitlab, gitlab_fallback_user, usermap)
    # Farewell
    LOG.info('done migration of project %s to GitLab ver. %s', gitlab_version, gitlab_project_name)
