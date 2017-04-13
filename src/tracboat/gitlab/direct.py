# -*- coding: utf-8 -*-

import os
import shutil
import logging
from datetime import datetime

from . import ConnectionBase, get_project_components

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
    'noteable_type': 'Issue',
}


class Connection(ConnectionBase):
    def __init__(self, project_name, db_model, db_connector, uploads_path,
                 create_missing=False): # TODO add project and namespace creation kwargs
        super(Connection, self).__init__(project_name)
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
        if create_missing and not self._get_project(self.project_name, self.project_namespace):
            LOG.debug("project %r doesn't exist, creating...", project_name)
            # TODO check for existing namespace
            if self.project_namespace:
                db_namespace = \
                    self.model.Namespaces.create(name=self.project_name,
                                                 path=self.project_namespace,
                                                 **NAMESPACE_DEFAULTS)
                db_namespace.save()
                namespace_id = db_namespace.id
                LOG.debug("namespace %r created", self.project_namespace)
            else:
                namespace_id = None
            db_project = self.model.Projects.create(name=self.project_name,
                namespace=namespace_id, **PROJECT_DEFAULTS)
            db_project.save()
            LOG.debug("project %r created in namespace %r",
                      self.project_name, self.project_namespace)

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

    def get_user_id(self, email):
        M = self.model
        return M.Users.get(M.Users.email == email).id
        # if email:
        #     return M.Users.get(M.Users.email == email).id
        # elif username:
        #     return M.Users.get(M.Users.username == username).id

    # def get_issues_iid(self):
    #     M = self.model
    #     return M.Issues.select().where(
    #         M.Issues.project == self.project_id).aggregate(
    #             peewee.fn.Count(M.Issues.id)) + 1

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

    def create_milestone(self, **kwargs):
        M = self.model
        # fix foreign keys
        kwargs['project'] = self.project_id
        kwargs['created_at'] = datetime.now()
        kwargs['updated_at'] = datetime.now()
        try:
            milestone = M.Milestones.get(
                (M.Milestones.title == kwargs['title']) &
                (M.Milestones.project == kwargs['project']))
            # for k in new_milestone._data:
            #     if k not in ('id', 'iid'):
            #         existing._data[k] = new_milestone._data[k]
            # new_milestone = existing
        except M.Milestones.DoesNotExist:
            milestone = M.Milestones.create(**kwargs)
            milestone.save()
            # new_milestone.iid = M.Milestones.select().where(
            #     M.Milestones.project == self.project_id).aggregate(
            #         peewee.fn.Count(M.Milestones.id)) + 1
        return milestone.id

    def create_issue(self, **kwargs):
        M = self.model
        # 1. Issue
        # fix foreign keys
        kwargs['project'] = self.project_id
        if 'milestone' in kwargs:
            kwargs['milestone'] = self.get_milestone_id(kwargs['milestone'])
        if 'author' in kwargs:
            kwargs['author'] = self.get_user_id(kwargs['author'])
        if 'assignee' in kwargs:
            kwargs['assignee'] = self.get_user_id(kwargs['assignee'])
        issue = M.Issues.create(**kwargs)
        issue.save()
        # 2. Event
        event = M.Events.create(
            action=1,
            author=issue.author,
            created_at=issue.created_at,
            project=issue.project,
            target=issue.id,
            target_type='Issue',
            updated_at=issue.created_at
        )
        event.save()
        # 3. Labels
        # TODO move label creation in a separate method
        for title in issue.labels.split(','):
            try:
                label = M.Labels.get((M.Labels.title == title) &
                                     (M.Labels.project == self.project_id))
            except M.Labels.DoesNotExist:
                label = M.Labels.create(
                    title=title,
                    color='#0000FF',
                    project=issue.project,
                    type='ProjectLabel',
                    created_at=issue.created_at,
                    update_at=issue.created_at
                )
                label.save()
            label_link = M.LabelLinks.create(
                label=label.id,
                target=issue.id,
                target_type='Issue',
                created_at=issue.created_at,
                update_at=issue.created_at
            )
            label_link.save()
        return issue.id

    def comment_issue(self, issue_id=None, binary_attachment=None, **kwargs):
        M = self.model
        # 1. Note
        # fix foreign keys
        kwargs['project'] = self.project_id
        if issue_id:
            kwargs['noteable'] = issue_id
        if 'author' in kwargs:
            kwargs['author'] = self.get_user_id(kwargs['author'])
        if 'updated_by' in kwargs:
            kwargs['updated_by'] = self.get_user_id(kwargs['updated_by'])
        # Fix defaults for non-null fields
        opts = dict(NOTE_DEFAULTS)
        opts.update(kwargs)
        # Create
        note = M.Notes.create(**opts)
        note.save()
        # 2. Event
        event = M.Events.create(
            action=1,
            author=note.author,
            created_at=note.created_at,
            project=note.project,
            target=note.id,
            target_type='Note',
            updated_at=note.created_at
        )
        event.save()
        # 3. Handle binary attachment if present
        if binary_attachment:
            directory = os.path.join(self.uploads_path, 'note/attachment/%s' % note.id)
            if not os.path.exists(directory):
                os.makedirs(directory)
            path = os.path.join(directory, note.attachment)
            with open(path, "wb") as f:
                f.write(binary_attachment)
        return note.id

    def save_wiki_attachment(self, path, binary):
        filename = os.path.join(self.uploads_path, self.project_qualname, path)
        if os.path.isfile(filename):
            raise Exception("file already exists: %r" % filename)
        directory = os.path.dirname(filename)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(filename, "wb") as f:
            f.write(binary)
