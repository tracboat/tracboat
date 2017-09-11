# -*- coding: utf-8 -*-

import abc
from os import path

import six

__all__ = [
    'ConnectionBase',
    'get_project_components',
]


def get_project_components(project_name):
    components = path.normpath(project_name).split(path.sep)
    return components[-1].strip(), filter(bool, (c.strip() for c in components[:-1]))


@six.add_metaclass(abc.ABCMeta)
class ConnectionBase(object):

    def __init__(self, project_name):
        project = project_name.strip()
        if not project:
            raise ValueError('invalid project name: {!r}'.format(project_name))
        p_name, p_groups = get_project_components(project_name)
        # TODO support for subgroups
        # In the meantime we are just creating a group joining all components
        # in a single identifier
        p_namespace = '/'.join(p_groups)
        self._project_name = p_name
        self._project_namespace = p_namespace

    @property
    def project_name(self):
        return self._project_name

    @property
    def project_namespace(self):
        return self._project_namespace

    @property
    def project_qualname(self):
        return (self.project_namespace + '/' if self.project_namespace else '') + \
               self.project_name

    @property
    def project_id(self):
        if not hasattr(self, '_project_id'):
            # pylint: disable=attribute-defined-outside-init
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
    def create_milestone(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def close_milestone(self, milestone_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_issue(self, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_user(self, email, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def comment_issue(self, issue_id=None, binary_attachment=None, **kwargs):
        raise NotImplementedError()

    @abc.abstractmethod
    def save_attachment(self, outpath, binary):
        raise NotImplementedError()
