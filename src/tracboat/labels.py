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

class LabelSet():
    def __init__(self):
        self.labels = {}
        self.label_by_type = {}

    def __len__(self):
        return len(self.labels)

    def add(self, label):
        self.labels.update({label.title: label})
        self.label_by_type[label.TYPE] = label

    def values(self):
        return self.labels.values()

    def add_many(self, labels):
        for label in labels:
            self.add(label)

    def get_status_label(self):
        return self.label_by_type[LabelStatus.TYPE]

    def get_label_titles(self):
        return [x.title for x in self.values()]

# class handling labels management
# when in trac we have 
# then in gitlab we have just labels
class LabelManager():
    def __init__(self, gitlab, logger):
        self.gitlab = gitlab
        self.logger = logger
        self.issues = {}

    def collect_labels(self, tickets):
        """
        Walk over tickets list,
        caches result in ticket object "labels" key.
        """

        self.logger.info('Labels: process %d tickets', len(tickets))
        # labels of all issues
        labels = LabelSet()
        for ticket_id, ticket in six.iteritems(tickets):
            if not 'labels' in ticket:
                ticket['labels'] = self.ticket_labels(ticket)
            labels.add_many(ticket['labels'].values())

        return labels

    def create_labels(self, tickets):
        """
        Create Labels in gitlab.
        Caches result in ticket object "labels" key.
        """

        labels = self.collect_labels(tickets)
        self.logger.info('Labels: Create %d labels', len(labels))

        for label in labels.values():
            self.gitlab.create_label(label)

    def ticket_labels(self, ticket):
        """
        Get labels related to Trac ticket
        """

        labels = LabelSet()
        classes = [
            LabelPriority,
            LabelResolution,
            LabelVersion,
            LabelComponent,
            LabelType,
            LabelStatus,
        ]

        for cls in classes:
            gen = self.factory(cls, ticket)
            labels.add_many(gen)

        return labels

    def factory(self, cls, ticket):
        for title in cls.from_ticket(ticket):
            if title != '':
                yield cls(title)
