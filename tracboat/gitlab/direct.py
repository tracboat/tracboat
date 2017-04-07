# -*- coding: utf-8 -*-

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python fileencoding=utf-8
'''
Copyright © 2013 - 2014
    Eric van der Vlist <vdv@dyomedea.com>
    Jens Neuhalfen <http://www.neuhalfen.name/>
See license information at the bottom of this file
'''

import os
import shutil
import importlib
from datetime import datetime

import six


__all__ = ['Connection']


class Connection(object):
    """
    Connection to the gitlab database
    """

    def __init__(self, project, uploads_path, db_model, db_connector):
        self.model = db_model
        self.model.database_proxy.initialize(db_connector)
        # peewee.PostgresqlDatabase(db_name, user=db_user, password=db_password, host=db_path)
        self.uploads_path = uploads_path
        self.project_name = project

    def clear_issues(self, project_id):
        M = self.model
        # Delete all the uses of the labels of the project.
        for label in M.Labels.select().where( M.Labels.project == project_id ):
            M.LabelLinks.delete().where( M.LabelLinks.label == label.id ).execute()
            ## You probably do not want to delete the labels themselves, otherwise you'd need to
            ## set their colour every time when you re-run the migration.
            #label.delete_instance()

        # Delete issues and everything that goes with them...
        for issue in M.Issues.select().where(M.Issues.project == project_id):
            for note in M.Notes.select().where( (M.Notes.project == project_id) & (M.Notes.noteable_type == 'Issue') & (M.Notes.noteable == issue.id)):
                if note.attachment != None:
                    directory = os.path.join(self.uploads_path, 'note/attachment/%s' % note.id)
                    try:
                        shutil.rmtree(directory)
                    except:
                        pass
                M.Events.delete().where( (M.Events.project == project_id) & (M.Events.target_type == 'Note' ) & (M.Events.target == note.id) ).execute()
                note.delete_instance()

            M.Events.delete().where( (M.Events.project == project_id) & (M.Events.target_type == 'Issue' ) & (M.Events.target == issue.id) ).execute()
            issue.delete_instance()

        M.Milestones.delete().where( M.Milestones.project == project_id ).execute()

    def milestone_by_name(self, project_id, milestone_name):
        M = self.model
        for milestone in M.Milestones.select().where((M.Milestones.title == milestone_name) & (M.Milestones.project == project_id)):
            return milestone._data
        return None

    def project_by_name(self, project_name):
        M = self.model
        (namespace, name) = project_name.split('/')
        print(name)
        for project in M.Projects.select().join(M.Namespaces, on=(M.Projects.namespace == M.Namespaces.id )).where((M.Projects.path == name) & (M.Namespaces.path == namespace)):
            print(project._data)
            return project._data
        return None

    def project_id(self):
        return self.project_id_by_name(self.project_name)

    def project_id_by_name(self, project_name):
        project = self.project_by_name(project_name)
        if not project:
            raise ValueError("Project '%s' not found" % project_name)
        return project["id"]

    def milestone_id_by_name(self, project_id, milestone_name):
        milestone = self.milestone_by_name(project_id, milestone_name)
        if not milestone:
            raise ValueError("Milestone '%s' of project '%s' not found" % (milestone_name, project_id))
        return milestone["id"]

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


'''
This file is part of <https://gitlab.dyomedea.com/vdv/trac-to-gitlab>.

This sotfware is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This sotfware is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with this library. If not, see <http://www.gnu.org/licenses/>.
'''
