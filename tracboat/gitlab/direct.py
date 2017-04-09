# -*- coding: utf-8 -*-

import os
import shutil
import logging
from datetime import datetime

import six
import peewee

from . import ConnectionBase, split_project_components

__all__ = ['Connection']


LOG = logging.getLogger(__name__)


# TODO infer correct defaults for non-null fields from an actual gitlab database
PROJECT_DEFAULTS = {
    'archived': False,
    'build_allow_git_fetch': True,
    'build_timeout': 0,
    'only_allow_merge_if_pipeline_succeeds': False,
    'public_builds': False,
    'repository_storage': 'TODO',
    'request_access_enabled': True,
    'shared_runners_enabled': True,
    'star_count': 0,
    'visibility_level': 0,

}

# TODO infer correct defaults for non-null fields from an actual gitlab database
NAMESPACE_DEFAULTS = {
    'description': 'imported',
    'request_access_enabled': True,
    'visibility_level': 0,
}


# TODO infer correct defaults for non-null fields from an actual gitlab database
USER_DEFAULTS = {
    'admin': False,
    'can_create_group': True,
    'can_create_team': True,
    'color_scheme': 0,
    # 'username'
    # 'email' = '',
    # 'encrypted_password' = CharField()
    'ldap_email': False,
    'linkedin': '',
    'otp_required_for_login': False,
    # 'public_email': ''
    'skype': '',
    'twitter': '',
    'website_url': '',
}


# TODO infer correct defaults for non-null fields from an actual gitlab database
NOTE_DEFAULTS = {
    'system': False,
}

class Connection(ConnectionBase):
    def __init__(self, project_name, db_model, db_connector, uploads_path,
                 create_missing=False): # TODO add project and namespace creation kwargs
        self.model = db_model
        self.model.database_proxy.initialize(db_connector)
        self.uploads_path = uploads_path
        # Ensure all needed tables are present
        self.model.Projects.create_table(fail_silently=True)
        self.model.Namespaces.create_table(fail_silently=True)
        self.model.Milestones.create_table(fail_silently=True)
        self.model.Events.create_table(fail_silently=True)
        self.model.Labels.create_table(fail_silently=True)
        self.model.Users.create_table(fail_silently=True)
        self.model.Issues.create_table(fail_silently=True)
        self.model.LabelLinks.create_table(fail_silently=True)
        self.model.Notes.create_table(fail_silently=True)
        # If requested, ensure namespace and project are present
        p_namespace, p_name = split_project_components(project_name)
        if create_missing and not self._get_project(p_namespace, p_name):
            LOG.debug("project %r doesn't exist, creating...", project_name)
            # TODO check for existing namespace
            if p_namespace:
                db_namespace = self.model.Namespaces.create(name=p_namespace,
                    path=p_namespace, **NAMESPACE_DEFAULTS)
                db_namespace.save()
                namespace_id = db_namespace.id
                LOG.debug("namespace %r created", p_namespace)
            else:
                namespace_id = None
            db_project = self.model.Projects.create(name=p_name,
                namespace=namespace_id, **PROJECT_DEFAULTS)
            db_project.save()
            LOG.debug("project %r created in namespace %r", p_name, p_namespace)
        super(Connection, self).__init__(project_name)

    def _get_project_id(self, project_name):
        project = self._get_project(project_name)
        if not project:
            raise ValueError("Project {!r} not found".format(project_name))
        return project["id"]

    def _get_project(self, p_name, p_namespace=None):
        M = self.model
        try:
            if p_namespace:
                project = M.Projects.select() \
                    .join(M.Namespaces, on=(M.Projects.namespace == M.Namespaces.id)) \
                    .where((M.Projects.path == p_name) &  # TODO why path is used as an identifier? Investigate!
                           (M.Namespaces.path == p_namespace)).get()
            else:
                project = M.Projects.select().where(M.Projects.name == p_name).get()
            return project._data
        except M.Projects.DoesNotExist:
            return None

    def clear_issues(self):
        M = self.model
        # Delete all the uses of the labels of the project.
        for label in M.Labels.select().where(M.Labels.project == self.project_id):
            M.LabelLinks.delete().where(M.LabelLinks.label == label.id).execute()
            ## You probably do not want to delete the labels themselves, otherwise you'd need to
            ## set their colour every time when you re-run the migration.
            # label.delete_instance()
        # Delete issues and everything that goes with them...
        for issue in M.Issues.select().where(M.Issues.project == self.project_id):
            for note in M.Notes.select().where(
                        (M.Notes.project == self.project_id) &
                        (M.Notes.noteable_type == 'Issue') &
                        (M.Notes.noteable == issue.id)):
                if note.attachment is not None:
                    directory = os.path.join(self.uploads_path, 'note/attachment/%s' % note.id)
                    shutil.rmtree(directory, ignore_errors=True)
                M.Events.delete().where(
                    (M.Events.project == self.project_id) &
                    (M.Events.target_type == 'Note') &
                    (M.Events.target == note.id)).execute()
                note.delete_instance()
            M.Events.delete().where(
                (M.Events.project == self.project_id) &
                (M.Events.target_type == 'Issue') &
                (M.Events.target == issue.id)).execute()
            issue.delete_instance()
        M.Milestones.delete().where(
            M.Milestones.project == self.project_id).execute()

    def get_milestone(self, milestone_name):
        M = self.model
        try:
            milestone = M.Milestones.select().where(
                (M.Milestones.title == milestone_name) &
                (M.Milestones.project == self.project_id)).get()
            return milestone._data if milestone else None
        except M.Milestones.DoesNotExist:
            return None

    def get_project(self):
        return self._get_project(self.project_name)

    def get_milestone_id(self, milestone_name):
        milestone = self.get_milestone(milestone_name)
        return milestone["id"] if milestone else None

    def get_user_id(self, email=None, username=None):
        M = self.model
        if email:
            return M.Users.get(M.Users.email == email).id
        elif username:
            return M.Users.get(M.Users.username == username).id

    def get_issues_iid(self):
        M = self.model
        return M.Issues.select().where(
            M.Issues.project == self.project_id).aggregate(
                peewee.fn.Count(M.Issues.id)) + 1

    def create_user(self, email, **kwargs):
        M = self.model
        try:
            user = M.Users.get(M.Users.email == email)
        except M.Users.DoesNotExist:
            parms = dict(USER_DEFAULTS)
            parms.update(kwargs)
            parms['email'] = email
            parms.setdefault('public_email', email)
            user = M.Users.create(**parms)
            user.save()
            LOG.debug("user %r created", email)
        return user.id

    def create_milestone(self, new_milestone):
        M = self.model
        try:
            existing = M.Milestones.get(
                (M.Milestones.title == new_milestone.title) &
                (M.Milestones.project == self.project_id))
            for k in new_milestone._data:
                if k not in ('id', 'iid'):
                    existing._data[k] = new_milestone._data[k]
            new_milestone = existing
        except:
            new_milestone.iid = M.Milestones.select().where(
                M.Milestones.project == self.project_id).aggregate(
                    peewee.fn.Count(M.Milestones.id)) + 1
            new_milestone.created_at = datetime.now()
            new_milestone.updated_at = datetime.now()
        new_milestone.save()
        return new_milestone

    def create_issue(self, new_issue):
        M = self.model
        new_issue.save()
        event = M.Events.create(
            action=1,
            author=new_issue.author,
            created_at=new_issue.created_at,
            project=self.project_id,
            target=new_issue.id,
            target_type='Issue',
            updated_at=new_issue.created_at
        )
        event.save()
        for title in set(new_issue.labels.split(',')):
            try:
                label = M.Labels.get((M.Labels.title == title) &
                                     (M.Labels.project == self.project_id))
            except:
                label = M.Labels.create(
                    title=title,
                    color='#0000FF',
                    project=self.project_id,
                    type='ProjectLabel',
                    created_at=new_issue.created_at,
                    update_at=new_issue.created_at
                )
                label.save()
            label_link = M.LabelLinks.create(
                label=label.id,
                target=new_issue.id,
                target_type='Issue',
                created_at=new_issue.created_at,
                update_at=new_issue.created_at
            )
            label_link.save()
        return new_issue

    def comment_issue(self, ticket, note, binary_attachment=None):
        M = self.model
        note.project = self.project_id
        note.noteable = ticket.id
        note.noteable_type = 'Issue'
        # Fix non-null fields
        # TODO this stuff must be refactored
        # entities must be handled here and not outside by the user
        for k, v in six.iteritems(NOTE_DEFAULTS):
            setattr(note, k, v)
        note.save()
        if binary_attachment:
            directory = os.path.join(self.uploads_path, 'note/attachment/%s' % note.id)
            if not os.path.exists(directory):
                os.makedirs(directory)
            path = os.path.join(directory, note.attachment)
            with open(path, "wb") as f:
                f.write(binary_attachment)
        event = M.Events.create(
            action=1,
            author=note.author,
            created_at=note.created_at,
            project=self.project_id,
            target=note.id,
            target_type='Note',
            updated_at=note.created_at
        )
        event.save()

    def save_wiki_attachment(self, path, binary):
        full_path = os.path.join(self.uploads_path, self.project_name, 'migrated', path)
        if os.path.isfile(full_path):
            raise Exception("file already exists: %s" % full_path)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(full_path, "wb") as f:
            f.write(binary)
