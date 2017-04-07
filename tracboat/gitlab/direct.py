# -*- coding: utf-8 -*-

import os
import shutil
import importlib
from datetime import datetime

import six

from . import ConnectionBase


__all__ = ['Connection']


class Connection(ConnectionBase):

    def __init__(self, project_name, db_model, db_connector, uploads_path):
        self.model = db_model
        self.model.database_proxy.initialize(db_connector)
        self.uploads_path = uploads_path
        super(Connection, self).__init__(project_name)

    def _get_project_id(self, project_name):
        project = self.project_by_name(project_name)
        if not project:
            raise ValueError("Project {!r} not found".format(project_name))
        return project["id"]

    def clear_issues(self):
        M = self.model
        # Delete all the uses of the labels of the project.
        for label in M.Labels.select().where(M.Labels.project == self.project_id):
            M.LabelLinks.delete().where(M.LabelLinks.label == label.id).execute()
            ## You probably do not want to delete the labels themselves, otherwise you'd need to
            ## set their colour every time when you re-run the migration.
            #label.delete_instance()
        # Delete issues and everything that goes with them...
        for issue in M.Issues.select().where(M.Issues.project == self.project_id):
            for note in M.Notes.select().where(
                (M.Notes.project == self.project_id) & \
                (M.Notes.noteable_type == 'Issue') & \
                (M.Notes.noteable == issue.id)):
                if note.attachment != None:
                    directory = os.path.join(self.uploads_path, 'note/attachment/%s' % note.id)
                    shutil.rmtree(directory, ignore_errors=True)
                M.Events.delete().where(
                    (M.Events.project == self.project_id) & \
                    (M.Events.target_type == 'Note') & \
                    (M.Events.target == note.id)).execute()
                note.delete_instance()
            M.Events.delete().where(
                (M.Events.project == self.project_id) & \
                (M.Events.target_type == 'Issue') & \
                (M.Events.target == issue.id)).execute()
            issue.delete_instance()
        M.Milestones.delete().where(
            M.Milestones.project == self.project_id).execute()

    def get_milestone(self, milestone_name):
        M = self.model
        for milestone in M.Milestones.select().where(  # TODO why a loop here?
                (M.Milestones.title == milestone_name) & \
                (M.Milestones.project == project_id)):
            return milestone._data
        return None

    def get_project(self):
        M = self.model
        (namespace, name) = self.project_name.split('/')  # TODO provide namespace and name at baseclass level
        for project in M.Projects.select().join(M.Namespaces,    # TODO why a loop here?
                on=(M.Projects.namespace == M.Namespaces.id )).where(
                    (M.Projects.path == name) & (M.Namespaces.path == namespace)):
            return project._data
        return None

    def get_milestone_id(self, milestone_name):
        milestone = self.get_milestone(self.project_id, milestone_name)
        return milestone["id"] if milestone else None

    def get_user_id(self, username):
        M = self.model
        return M.Users.get(M.Users.username == username).id

    def get_issues_iid(self, dest_project_id):
        M = self.model
        return M.Issues.select().where(M.Issues.project == dest_project_id).aggregate(fn.Count(M.Issues.id)) + 1

    def create_milestone(self, dest_project_id, new_milestone):
        M = self.model
        try:
            existing = M.Milestones.get((M.Milestones.title == new_milestone.title) & (M.Milestones.project == dest_project_id))
            for k in new_milestone._data:
                if k not in ('id', 'iid'):
                    existing._data[k] = new_milestone._data[k]
            new_milestone = existing
        except:
            new_milestone.iid = M.Milestones.select().where(M.Milestones.project == dest_project_id).aggregate(fn.Count(M.Milestones.id)) + 1
            new_milestone.created_at = datetime.now()
            new_milestone.updated_at = datetime.now()
        new_milestone.save()
        return new_milestone

    def create_issue(self, dest_project_id, new_issue):
        M = self.model
        new_issue.save()
        event = M.Events.create(
            action=1,
            author=new_issue.author,
            created_at=new_issue.created_at,
            project=dest_project_id,
            target=new_issue.id,
            target_type='Issue',
            updated_at=new_issue.created_at
        )
        event.save()
        for title in set(new_issue.labels.split(',')):
            try:
                label = M.Labels.get((M.Labels.title == title) & (M.Labels.project == dest_project_id))
            except:
                label = M.Labels.create(
                    title=title,
                    color='#0000FF',
                    project=dest_project_id,
                    type='ProjectLabel',
                    created_at=new_issue.created_at,
                    update_at=new_issue.created_at
                )
                label.save()
            label_link = LabelLinks.create(
                label=label.id,
                target=new_issue.id,
                target_type='Issue',
                created_at=new_issue.created_at,
                update_at=new_issue.created_at
            )
            label_link.save()
        return new_issue

    def comment_issue(self, project_id, ticket, note, binary_attachment):
        M = self.model
        note.project = project_id
        note.noteable = ticket.id
        note.noteable_type = 'Issue'
        note.save()

        if binary_attachment:
            directory = os.path.join(self.uploads_path, 'note/attachment/%s' % note.id)
            if not os.path.exists(directory):
                os.makedirs(directory)
            path = os.path.join(directory, note.attachment)
            f = open(path, "wb")
            f.write(binary_attachment)
            f.close()

        event = M.Events.create(
            action=1,
            author=note.author,
            created_at=note.created_at,
            project=project_id,
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
        f = open(full_path, "wb")
        f.write(six.b(binary))
        f.close()
