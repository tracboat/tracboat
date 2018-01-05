# -*- coding: utf-8 -*-

import six
from pprint import pprint

class LabelAbstract():
    TYPE = None
    COLOR = None
    MAPPING = {}

    def __init__(self, title):
        if title in self.MAPPING:
            self.title = self.MAPPING[title]
        else:
            self.title = title

    @staticmethod
    def from_ticket(ticket):
        """
        yield possible names from trac ticket
        """
        pass

class LabelPriority(LabelAbstract):
    TYPE = 'priority'
    COLOR = '#D9534F'

    @staticmethod
    def from_ticket(ticket):
        try:
            yield ticket['attributes']['priority']
        except KeyError:
            pass

class LabelResolution(LabelAbstract):
    TYPE = 'resolution'
    COLOR = '#AD8D43'

    @staticmethod
    def from_ticket(ticket):
        try:
            yield ticket['attributes']['resolution']
        except KeyError:
            pass

        # get versions from changelog
        for change in ticket['changelog']:
            if change['field'] == 'resolution':
                yield change['oldvalue']
                yield change['newvalue']

class LabelVersion(LabelAbstract):
    TYPE = 'version'
    COLOR = '#5CB85C'

    @staticmethod
    def from_ticket(ticket):
        try:
            yield ticket['attributes']['version']
        except KeyError:
            pass

        # get versions from changelog
        for change in ticket['changelog']:
            if change['field'] == 'version':
                yield change['oldvalue']
                yield change['newvalue']

class LabelComponent(LabelAbstract):
    TYPE = 'component'
    COLOR = '#8E44AD'

    @staticmethod
    def from_ticket(ticket):
        try:
            components = ticket['attributes']['component'].split(',')
        except KeyError:
            return

        for comp in components:
            yield comp

class LabelType(LabelAbstract):
    TYPE = 'type'
    COLOR = '#A295D6'

    @staticmethod
    def from_ticket(ticket):
        try:
            yield ticket['attributes']['type']
        except KeyError:
            pass

class LabelStatus(LabelAbstract):
    TYPE = 'state'
    COLOR = '#0033CC'
    MAPPING = {
        'new': 'opened',
        'assigned': 'opened',
        'accepted': 'opened',
        'reopened': 'opened',
        'closed': 'closed',
    }

    @staticmethod
    def from_ticket(ticket):
        try:
            yield ticket['attributes']['status']
        except KeyError:
            pass

        for change in ticket['changelog']:
            if change['field'] == 'status':
                yield change['oldvalue']
                yield change['newvalue']


# class handling labels management
# when in trac we have 
# then in gitlab we have just labels
class LabelManager():
#    LABEL_PRIORITY = 'priority'
#    LABEL_RESOLUTION = 'resolution'
#    LABEL_VERSION = 'version'
#    LABEL_COMPONENT = 'component'
#    LABEL_TYPE = 'type'
#    LABEL_STATE = 'state'

    def __init__(self, gitlab, logger):
        self.gitlab = gitlab
        self.logger = logger
        self.issues = {}

    def create_labels(self, tickets):
        """
        Create Labels in gitlab
        """
        self.logger.info('Labels: process %d tickets', len(tickets))
        for ticket_id, ticket in six.iteritems(tickets):
            labels = self.ticket_labels(ticket)
            pprint([x for x in labels])

    def ticket_labels(self, ticket):
        """
        Get labels related to Trac ticket
        """

        labels = []
        labels.extend([x for x in self.factory(LabelPriority, ticket)])
        labels.append([x for x in self.factory(LabelResolution, ticket)])
        labels.append([x for x in self.factory(LabelVersion, ticket)])
        labels.append([x for x in self.factory(LabelComponent, ticket)])
        labels.append([x for x in self.factory(LabelType, ticket)])
        labels.append([x for x in self.factory(LabelStatus, ticket)])
#
#        labels = priority_labels | resolution_labels | version_labels | \
#            component_labels | type_labels | state_labels | note_labels
#        labels = priority_labels

        return labels

    def factory(self, cls, ticket):
        for title in cls.from_ticket(ticket):
            if title != '':
                yield cls(title)

TICKET_PRIORITY_TO_ISSUE_LABEL = {
    'high': 'priority:high',
    'minor': 'priority:minor',
    'critical': 'priority:critical',
    'blocker': 'priority:blocker',
    # 'medium': None,
    'major': 'priority:major',
    'low': 'priority:low',
    'trivial': 'priority:trivial',
}
