# -*- coding: utf-8 -*-

import logging
import os
import random
import re
import string
import difflib
from itertools import chain
from sys import exit
from pprint import pprint

import six

from tracboat import trac2down
from tracboat.gitlab import direct  # TODO selectable mode (api/direct)
from tracboat.gitlab import model

__all__ = ['migrate']

LOG = logging.getLogger(__name__)
#logging.basicConfig(filename='comment.log', filemode='w', level=logging.INFO)

TICKET_PRIORITY_TO_ISSUE_LABEL = {
    'high': 'priority:high',
    'minor': 'priority:minor',
    'critical': 'priority:critical',
    # 'medium': None,
    'major': 'priority:major',
    'low': 'priority:low',
}

TICKET_RESOLUTION_TO_ISSUE_LABEL = {
    'fixed': 'closed:fixed',
    'invalid': 'closed:invalid',
    'wontfix': 'closed:wontfix',
    'duplicate': 'closed:duplicate',
    'worksforme': 'closed:worksforme',
}

TICKET_STATE_TO_ISSUE_STATE = {
    'new': 'opened',
    'assigned': 'opened',
    'accepted': 'opened',
    'reopened': 'opened',
    'closed': 'closed',
}

################################################################################
# Wiki format normalization
################################################################################

CHANGESET_REX = re.compile(
    r'(?sm)In \[changeset:"([^"/]+?)(?:/[^"]+)?"\]:\n\{\{\{(\n#![^\n]+)?\n(.*?)\n\}\}\}'
)

CHANGESET2_REX = re.compile(
    r'\[changeset:([a-zA-Z0-9]+)\]'
)


def _format_changeset_comment(rex):
    return 'In changeset ' + rex.group(1) + ':\n> ' + rex.group(3).replace('\n', '\n> ')


def _wikifix(text):
    text = CHANGESET_REX.sub(_format_changeset_comment, text)
    text = CHANGESET2_REX.sub(r'\1', text)
    return text


def _wikiconvert(text, basepath, multiline=True, note_map={}, attachments_path=None, svn2git_revisions={}):
    return trac2down.convert(_wikifix(text), basepath, multiline, note_map=note_map, attachments_path=attachments_path, svn2git_revisions=svn2git_revisions)


################################################################################
# Trac ticket metadata conversion
################################################################################

def gitlab_priority_label(priority, priority_to_label=None):
    priority_to_label = priority_to_label or TICKET_PRIORITY_TO_ISSUE_LABEL
    if priority in priority_to_label:
        return priority_to_label[priority]
    else:
        # todo find a meaningful default value for unknown resolutions
        raise ValueError('no label for {} priority'.format(priority))

def ticket_priority(ticket, priority_to_label=None):
    priority_to_label = priority_to_label or TICKET_PRIORITY_TO_ISSUE_LABEL
    priority = ticket['attributes']['priority']
    if priority in priority_to_label:
        return {priority_to_label[priority]}
    else:
        return set()

def gitlab_resolution_label(resolution, resolution_to_label=None):
    resolution_to_label = resolution_to_label or TICKET_RESOLUTION_TO_ISSUE_LABEL
    if resolution in resolution_to_label:
        return resolution_to_label[resolution]
    else:
        # todo find a meaningful default value for unknown resolutions
        raise ValueError('no label for {} resolution'.format(resolution))

def ticket_resolution(ticket, resolution_to_label=None):
    resolution_to_label = resolution_to_label or TICKET_RESOLUTION_TO_ISSUE_LABEL
    resolution = ticket['attributes']['resolution']

    if resolution in resolution_to_label:
        return {resolution_to_label[resolution]}
    else:
        return set()


def version_label(version):
    return 'version:{}'.format(version)

def ticket_versions(ticket):
    labels = set()

    try:
        labels.add(version_label(ticket['attributes']['version']))
    except KeyError:
        pass

    def add_version(labels, version):
        if version == '':
            return
        labels.add(version_label(version))

    # get versions from changelog
    for change in ticket['changelog']:
        if change['field'] == 'version':
            add_version(labels, change['oldvalue'])
            add_version(labels, change['newvalue'])

    return labels

def ticket_components(ticket):
    components = ticket['attributes']['component'].split(',')
    return {'comp:{}'.format(comp.strip()) for comp in components}

def ticket_note_labels(ticket):
    labels = set()

    for change in ticket['changelog']:
        if not change['field'] in ['resolution', 'status']:
            continue

        if change['field'] == 'resolution':
            if change['newvalue'] == '':
                label = gitlab_resolution_label(change['oldvalue'])
                labels.add(label)
            else:
                label = gitlab_resolution_label(change['newvalue'])
                labels.add(label)

        if change['field'] == 'status':
            label = gitlab_status_label(change['oldvalue'])
            labels.add(label)
            label = gitlab_status_label(change['newvalue'])
            labels.add(label)

    return labels

def ticket_type(ticket):
    ttype = ticket['attributes']['type']
    return {'type:{}'.format(ttype.strip())}


def gitlab_status_label(status, status_to_state=None):
    status_to_state = status_to_state or TICKET_STATE_TO_ISSUE_STATE
    if status in status_to_state:
        return status_to_state[status]
    else:
        # todo find a meaningful default value for unknown statuses
        raise ValueError('no label for {} status'.format(status))


def ticket_state(ticket, status_to_state=None):
    status_to_state = status_to_state or TICKET_STATE_TO_ISSUE_STATE
    state = ticket['attributes']['status']
    if state in status_to_state:
        return status_to_state[state], set()
    else:
        return None, {'state:{}'.format(state)}


# https://stackoverflow.com/a/21790513
# https://stackoverflow.com/a/22043027
def render_text_diff(text1, text2):
    diff = difflib.ndiff(text1.splitlines(), text2.splitlines())
    return "```diff\n%s\n```\n" % "\n".join(diff)

# https://gitlab.com/gitlab-org/gitlab-ce/commit/00688e438c04e622a8afb96904b8724f8818f6ce#note_40208591
def render_html5_details(text, summary="Summary"):
    return """
<details>
<summary>%s</summary>
<pre>
%s
</pre>
</details>
""" % (summary, text)

################################################################################
# Trac dict -> GitLab dict conversion
# The GitLab dict is a GitLab model-friendly representation, the GitLab dict
# can be unrolled as kwargs to the corresponding database model entity
# e.g.:
#  dbmodel.Milestone(**milestone_kwargs(trac_milestone))
################################################################################

def identity_converter(value):
    return value

def format_label(value):
    return '~"%s"' % value

def format_emphasis(value):
    return '*%s*' % value

def format_milestone(value):
    return '%%"%s"' % value

def format_fieldchange(field_name, change, value_converter=identity_converter, format_converter=format_emphasis):
    change['field_name'] = field_name

    def converter(value):
        return format_converter(value_converter(value))

    if change['newvalue'] == '':
        change['oldvalue'] = converter(change['oldvalue'])
        note = '- **%(field_name)s** %(oldvalue)s deleted' % change
    elif change['oldvalue'] != '':
        change['oldvalue'] = converter(change['oldvalue'])
        change['newvalue'] = converter(change['newvalue'])
        note = '- **%(field_name)s** changed from %(oldvalue)s to %(newvalue)s' % change
    else:
        change['newvalue'] = converter(change['newvalue'])
        note = '- **%(field_name)s** set to %(newvalue)s' % change

    return note

def format_change_note(change, issue_id=None, note_map={}, svn2git_revisions={}):
    """
    format "note" for change
    """

    attachments_path = '/uploads/issue_%s' % issue_id
    field = change['field']

    if field == 'comment':
        note = _wikiconvert(change['newvalue'], '/issues/', multiline=False, note_map=note_map, attachments_path=attachments_path, svn2git_revisions=svn2git_revisions)
    elif field == 'resolution':
        note = format_fieldchange('Resolution', change, value_converter=gitlab_resolution_label, format_converter=format_label)
    elif field == 'priority':
        note = format_fieldchange('Priority', change, value_converter=gitlab_priority_label, format_converter=format_label)
    elif field == 'milestone':
        note = format_fieldchange('Milestone', change, format_converter=format_milestone)
    elif field == 'estimatedhours':
        note = format_fieldchange('Estimated Hours', change)
    elif field == 'summary':
        note = format_fieldchange('Summary', change)
    elif field == 'status':
        note = format_fieldchange('Status', change, value_converter=gitlab_status_label, format_converter=format_label)
    elif field == 'version':
        def converter(value):
            return 'version:%s' % value
        note = format_fieldchange('Version', change, value_converter=converter, format_converter=format_label)
    elif field == 'description':
        if change['oldvalue'] == '':
            # XXX: does this happen or we need only 'diff' render?
            note = '- **Description** changed\n\n%s' % render_html5_details(change['newvalue'])
        else:
            note = '- **Description** changed\n\n%s' % render_text_diff(change['oldvalue'], change['newvalue'])
    elif field == 'attachment':
        # ![20170905_134928](/uploads/f38feb8a3dc4c5bcabdc41ccc5894ac3/20170905_134928.jpg)
        # will be saved  relative to the project:
        # /var/opt/gitlab/gitlab-rails/uploads/glen/photoproject/f38feb8a3dc4c5bcabdc41ccc5894ac3
        note = '- **Attachment** [%s](%s/%s) added' % (change['newvalue'], attachments_path, change['newvalue'])
    elif field == 'cc':
        if change['newvalue'] == '':
            raise Exception('Unexpected empty value for %s' % field)

        note = '- **Cc** added @%s' % change['newvalue']
    elif field == 'owner':
        if change['oldvalue'] == '' and change['newvalue'] == '':
            # XXX no idea why such changes even exist
            note = ''
        elif change['newvalue'] == '':
            raise Exception('Unexpected empty value for %s' % field)

        note = '- **Owner** set to @%s' % change['newvalue']
    else:
        raise Exception('Unexpected field %s' % field)

    return note

def change_comment_kwargs(change, note):
    """
    called for change['field'] == 'comment'
    """

    return {
        'note': note,
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
    version_labels = ticket_versions(ticket)
    component_labels = ticket_components(ticket)
    type_labels = ticket_type(ticket)
    state, state_labels = ticket_state(ticket)
    note_labels = ticket_note_labels(ticket)

    labels = priority_labels | resolution_labels | version_labels | \
        component_labels | type_labels | state_labels | note_labels

    return {
        'title': ticket['attributes']['summary'],
        'description': _wikiconvert(ticket['attributes']['description'],
                                    '/issues/', multiline=False),
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
        # keep open, close later, to handle milestones being referred from comments
#        'state': 'closed' if milestone['completed'] else 'active',
        'state': 'active',
        'due_date': milestone['due'] if milestone['due'] else None,
        # References:
        # 'project': None,
    }


################################################################################
# Conversion API
################################################################################

def sort_changelog(changelog):
    # Even if the fields and comment have identical date, trac just formats them separately:
    # - fields
    # - comments
    # https://trac.edgewall.org/browser/tags/trac-1.0.15/trac/ticket/templates/ticket_change.html
    # {'author', 'field', 'newvalue', 'oldvalue', 'permanent', 'time'}
    # so sort by date and then items by field being comment
    return sorted(changelog, key = lambda obj: (obj['time'], 1 if obj['field'] == 'comment' else -1, obj['time']))

def merge_changelog(ticket_id, changelog):
    """
    Merge changes of type 'resolution' and 'status' into 'comment', because this is how Trac displays changes.

    Basically each 'comment' starts new post, otherwise grouped to same item.
    """

    notes = []
    last_change = None

    def insert_notes(change, notes):
        # first merge notes into
        if len(notes):
            # prepend existing notes
            change['newvalue'] = "\n".join(notes) + "\n\n" + change['newvalue']
        return change

    for change in sort_changelog(changelog):
        last_change = change
        if change['field'] in ['resolution', 'status', 'milestone', 'version', 'description', 'attachment', 'cc', 'summary', 'owner', 'estimatedhours', 'priority']:
            # just collect 'note', the rest is same anyway
            note = format_change_note(change, issue_id=ticket_id)
            if note == '':
                LOG.info('skip empty comment: change: %r', change)
                continue
            notes.append(note)
            continue

        if change['field'] == 'comment':
            # comment flushes
            # field type comment flushes
            yield insert_notes(change, notes)
            notes = []
            continue

        LOG.info('changelog: skip field: %s', change['field'])

    # last non-comments may need to be flushed as well
    if len(notes):
        yield insert_notes(last_change, notes)

def migrate_tickets(trac_tickets, gitlab, default_user, usermap=None, svn2git_revisions={}):
    LOG.info('MIGRATING %d tickets to issues', len(trac_tickets))

    for ticket_id, ticket in six.iteritems(trac_tickets):
        LOG.info('migrate #%d: %r', ticket_id, ticket)
        # trac note_id -> gitlab note_id
        note_map = {}
        trac_note_id = 1

        issue_args = ticket_kwargs(ticket)
        # Fix user mapping
        issue_args['author'] = usermap.get(issue_args['author'], default_user)
        issue_args['assignee'] = usermap.get(issue_args['assignee'], default_user)

        issue_args['iid'] = ticket_id

        LOG.info("TICKET: #%r: %r" % (ticket_id, ticket))
        LOG.info("ISSUE: %r" % issue_args)

        # Create
        gitlab_issue_id = gitlab.create_issue(**issue_args)
        LOG.info('migrated ticket %s -> %s', ticket_id, gitlab_issue_id)

        # migrate attachments from comments
        for filename, attachment in six.iteritems(ticket['attachments']):
            attrs = attachment['attributes']
            LOG.info('saving attachment: %s (%d bytes) author: %s, description: %s' % (filename, attrs['size'], attrs['author'], attrs['description']))
            gitlab.save_attachment('issue_%s/%s' % (ticket_id, filename), attachment['data'])

        # Migrate whole changelog
        LOG.info('changelog: %r', ticket['changelog'])
        for change in merge_changelog(ticket_id, ticket['changelog']):
            if change['field'] == 'comment':
                note = format_change_note(change, note_map=note_map, issue_id=ticket_id, svn2git_revisions=svn2git_revisions)
                if note == '':
                    LOG.info('skip empty comment: change: %r', change)
                    continue
                note_args = change_comment_kwargs(change, note)
                # Fix user mapping
                note_args['author'] = usermap.get(note_args['author'], default_user)
                note_args['updated_by'] = usermap.get(note_args['updated_by'], default_user)
                # TODO changelog binary attachments
                gitlab_note_id = gitlab.comment_issue( issue_id=gitlab_issue_id, binary_attachment=None, **note_args)
                LOG.info('migrated ticket #%s note: %r', ticket_id, gitlab_note_id)

                note_map[trac_note_id] = gitlab_note_id
                trac_note_id += 1
            else:
                # TODO: skip field: description
                # skip field: _comment0
                # skip field: component
                # skip field: parents
                # skip field: type
                LOG.info('skip field: %s', change['field'])

# for ticket comments to appear normally, we created all milestones as 'active'
# now close the milestones that are 'closed'
def close_milestones(trac_milestones, gitlab):
    closed_milestones = [milestone for milestone in six.itervalues(trac_milestones) if milestone['completed']]
    LOG.info('closing %d milestones', len(closed_milestones))
    for milestone in closed_milestones:
        milestone_id = gitlab.get_milestone_id(milestone['name'])
        gitlab.close_milestone(milestone_id)

def migrate_milestones(trac_milestones, gitlab):
    LOG.info('migrating %d milestones', len(trac_milestones))
    for title, milestone in six.iteritems(trac_milestones):
        milestone_args = milestone_kwargs(milestone)
        LOG.info('migrate milestone %r', milestone_args)
        gitlab_milestone_id = gitlab.create_milestone(**milestone_args)
        # => #<Milestone id: 2456,
#        title: "v1", project_id: 166, description: "", 
#due_date: nil, created_at: "2017-04-21 22:45:30", 
#updated_at: "2017-04-21 22:45:30", state: "active", 
#iid: 1, title_html: "v1", description_html: "", 
#start_date: nil>
        LOG.info('migrated milestone %s -> %s', title, gitlab_milestone_id)


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
            gitlab.save_attachment(name, data)
            converted_page = \
                converted_page.replace(r'migrated/%s)' % filename,
                                       r'migrated/%s)' % name)
            if '%s)' % name not in converted_page:
                orphaned.append(name)
            LOG.debug('migrated attachment %s @ %s', title, filename)
        # Add orphaned attachments to page
        if orphaned:
            converted_page += '\n\n'
            converted_page += '''
##### Orphaned attachments
##### These are the attachments files found but with no references
##### in the page contents.
##### During migration the following orphaned attachments have been found:
'''
            for filename in orphaned:
                converted_page += '- [%s](/uploads/migrated/%s)\n' % (filename, filename)
        # Writeout!
        trac2down.save_file(converted_page, title, version, last_modified, author, output_dir)
        LOG.debug('migrated wiki page %s', title)


def generate_password(length=None):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(alphabet) for _ in range(length or 30))

def create_users(gitlab, usermap, userattrs, gitlab_fallback_user):
    for email in chain(six.itervalues(usermap), [gitlab_fallback_user]):
        attrs = {  # set mandatory values to defaults
            'email': email,
            'username': email.split('@')[0],
            'encrypted_password': generate_password(),
            'two_factor_enabled' : False,
        }

        attrs.update(userattrs.get(email, {}))
        gitlab.create_user(**attrs)
        LOG.info('created GitLab user %r', email)
        LOG.debug('created GitLab user %r with attributes: %r', email, attrs)

# pylint: disable=too-many-arguments
def migrate(trac, gitlab_project_name, gitlab_version, gitlab_db_connector,
            output_wiki_path, output_uploads_path, gitlab_fallback_user,
            usermap=None, userattrs=None, svn2git_revisions={}):
    LOG.info('migrating project %r to GitLab ver. %s', gitlab_project_name, gitlab_version)
    LOG.info('uploads repository path is: %r', output_uploads_path)
    db_model = model.get_model(gitlab_version)
    LOG.info('retrieved database model for GitLab ver. %s: %r', gitlab_version, db_model.__file__)
    gitlab = direct.Connection(gitlab_project_name, db_model, gitlab_db_connector,
                               output_uploads_path, create_missing=False)
    LOG.info('estabilished connection to GitLab database')
    # 0. Users
    #create_users(gitlab, usermap, userattrs, gitlab_fallback_user)

    # XXX
    # if overwite and mode == direct
    # XXX: this clears also milestones
    # XXX: make configurable
    gitlab.clear_issues()

    # 1. Wiki
#    LOG.info('migrating %d wiki pages to: %s', len(trac['wiki']), output_wiki_path)
#    migrate_wiki(trac['wiki'], gitlab, output_wiki_path)
    # 2. Milestones
    migrate_milestones(trac['milestones'], gitlab)
    # 3. Issues
    migrate_tickets(trac['tickets'], gitlab, gitlab_fallback_user, usermap, svn2git_revisions=svn2git_revisions)
    #close_milestones(trac['milestones'], gitlab) - gitlab bug?
    # Farewell
    LOG.info('done migration of project %r to GitLab ver. %s', gitlab_project_name, gitlab_version)
