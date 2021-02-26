# -*- coding: utf-8 -*-

import logging
import six
import random
import string
from itertools import chain
from pprint import pprint

class UserManager():
    def __init__(self, gitlab, usermap={}, userattrs={}, fallback_user=None, create_users=False):
        self.gitlab = gitlab
        self.logger = logging.getLogger(__name__)
        self.usermap = usermap
        self.userattrs = userattrs
        self.fallback_user = fallback_user
        self.create_users = create_users

        # GitLab User Model objects
        self.users = {}

    def get_email(self, login):
        self.logger.debug("get_email:%s" % login)
        return self.users[login].email

    # trac_user_handle -> gitlab_user_handle
    def get_login(self, login, fallback=None):
        self.logger.debug("get_login:%s" % login)
#        try:
        return self.users[login].username
#        except KeyError:
#            return fallback

    def load_users(self, users):
        """
        Load Trac users into internal cache
        """

        for login in users:
            email = self.usermap.get(login, self.fallback_user)
            self.create_user(email)
            user = self.gitlab.get_user(email)
            self.logger.info("Load %s as %s: %r" % (login, email, user))
            self.users[login] = user

    def create_user(self, email):
        if self.gitlab.user_exists(email):
            return

        if not self.create_users:
            raise Exception('User creation disabled, no account for %r' % email)

        # set mandatory values to defaults
        attrs = {
            'email': email,
            'username': email.split('@')[0],
            'name': email.split('@')[0],
            'encrypted_password': self.generate_password(),
            'two_factor_enabled' : False,
        }

        attrs.update(self.userattrs.get(email, {}))
        self.gitlab.create_user(**attrs)
        self.logger.info('Created GitLab user %r', email)
        self.logger.debug('Created GitLab user %r with attributes: %r', email, attrs)

    def generate_password(self, length=None):
        alphabet = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(alphabet) for _ in range(length or 30))
