# -*- coding: utf-8 -*-

import abc

import six


__all__ = ['ConnectionBase']


@six.add_metaclass(abc.ABCMeta)
class ConnectionBase(object):

    def __init__(self, project_name):
        prj = project_name.strip()
        if not prj:
            raise ValueError('invalid project name: {!r}'.format(project_name))
        self._project_name = prj

    @property
    def project_name(self):
        return self.project_name

    @property
    def project_id(self):
        if not hasattr(self, '_project_id'):
            self._project_id = self._get_project_id(self.project_name)
        return self._project_id

    # Protected

    @abc.abstractmethod
    def _get_project_id(self, project_name):
        raise NotImplementedError()

    # Public API

    @abc.abstractmethod
    def clear_issues(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_milestone(self, milestone_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_project(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_milestone_id(self, milestone_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_user_id(self, username):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_issues_iid(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_milestone(self, new_milestone):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_issue(self, new_issue):
        raise NotImplementedError()

    @abc.abstractmethod
    def comment_issue(self, ticket, note, binary_attachment):
        raise NotImplementedError()

    @abc.abstractmethod
    def save_wiki_attachment(self, path, binary):
        raise NotImplementedError()
