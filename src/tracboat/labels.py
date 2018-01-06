# -*- coding: utf-8 -*-

import six
from pprint import pprint

class LabelAbstract():
    TYPE = None
    COLOR = None
    ATTRIBUTE_NAME = None
    MAPPING = {}

    def __init__(self, title):
        self.title = self.convert_value(title)

    @classmethod
    def convert_value(cls, title):
        if title in cls.MAPPING:
            return cls.MAPPING[title]
        else:
            return title

    @classmethod
    def from_ticket(cls, ticket):
        """
        yield possible names from trac ticket
        """
        attribute_name = cls.ATTRIBUTE_NAME
        try:
            values = ticket['attributes'][attribute_name].split(',')
        except KeyError:
            pass

        for value in values:
            yield value

        # get versions from changelog
        for change in ticket['changelog']:
            if change['field'] == attribute_name:
                yield change['oldvalue']
                yield change['newvalue']

class LabelPriority(LabelAbstract):
    TYPE = 'priority'
    COLOR = '#D9534F'
    ATTRIBUTE_NAME = 'priority'

class LabelResolution(LabelAbstract):
    TYPE = 'resolution'
    COLOR = '#AD8D43'
    ATTRIBUTE_NAME = 'resolution'

class LabelVersion(LabelAbstract):
    TYPE = 'version'
    COLOR = '#5CB85C'
    ATTRIBUTE_NAME = 'version'

class LabelComponent(LabelAbstract):
    TYPE = 'component'
    COLOR = '#8E44AD'
    ATTRIBUTE_NAME = 'component'

class LabelType(LabelAbstract):
    TYPE = 'type'
    COLOR = '#A295D6'
    ATTRIBUTE_NAME = 'type'

class LabelStatus(LabelAbstract):
    TYPE = 'status'
    COLOR = '#0033CC'
    ATTRIBUTE_NAME = 'status'
    MAPPING = {
        'new': 'opened',
        'assigned': 'opened',
        'accepted': 'opened',
        'reopened': 'opened',
        'closed': 'closed',
    }

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
