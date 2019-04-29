.. figure:: https://nazavode.github.io/img/lifeboat-banner.png
   :alt: image

TracBoat
========

|build-status| |coverage-status| |codeqa| |license-status|

A life boat to escape the Trac ocean liner.

**TracBoat** is a toolbox for exporting whole Trac instances, saving
them and migrating them to other platforms.

Features
--------

-  Export Trac projects along with issues, issue changelogs (with
   attachments) and wiki pages (with attachments)
-  Create GitLab users, projects and namespaces involved in the
   migration process
-  Export Trac projects to local files (in json, toml, Python literal or
   Python pickle formats)
-  Migrate Trac projects directly from remote instances as well as from
   previously created export files
-  Migrate Trac projects to a live GitLab instance
-  Migrate Trac projects to a mocked GitLab on the file system to check
   for correctness

Installation
------------

If you want to **install from source**, doing it in a ``virtualenv`` is
*highly recommended*. After having this repo cloned, just type:

.. code:: shell

    $ cd tracboat
    $ virtualenv -p python2.7 VENV
    $ source VENV/bin/activate
    $ pip install -r requirements/dist.txt
    $ pip install -e .

Alternatively with **pipenv**

.. code:: shell

    $ cd tracboat
    $ pip install pipenv
    $ pipenv install -e .
    $ pipenv run tracboat

Dependencies
------------

-  Tested on Python 2.7 and Python >= 3.4
-  `peewee <https://pypi.python.org/pypi/peewee>`__
-  `psycopg2 <https://pypi.python.org/pypi/psycopg2>`__
-  `six <https://pypi.python.org/pypi/six>`__
-  `click <https://pypi.python.org/pypi/click>`__
-  `toml <https://pypi.python.org/pypi/toml>`__
-  `pymongo <https://pypi.python.org/pypi/pymongo>`__

Getting started
---------------

Every command line option can be specified as an environment variable,
so the following command:

.. code:: shell

    $ tracboat users --trac-uri=https://mytrac/xmlrpc --no-ssl-verify

...is exactly the same as the following:

.. code:: shell

    $ export TRACBOAT_TRAC_URI=https://mytrac/xmlrpc
    $ export TRACBOAT_SSL_VERIFY=0
    $ tracboat users

Another way to conveniently configure ``tracboat`` is with a
configuration file in `TOML <https://github.com/toml-lang/toml>`__
format. Providing a file

.. code:: shell

    $ cat mytrac.toml
    [tracboat]
    trac_uri = "https://mytrac/xmlrpc"
    ssl_verify = false
    $ tracboat --config-file=mytrac.toml users

Please note that when a value is specified more that once, the priority
order considered is the following:

1. command line option;
2. environment variable;
3. configuration file;
4. default value.

If you are *very* curious about how to play with command line options,
have a look to the `click documentation <http://click.pocoo.org/>`__.

Collecting Trac users
~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    $ tracboat users --trac-uri=http://localhost/xmlrpc

Export a Trac instance
~~~~~~~~~~~~~~~~~~~~~~

.. code:: shell

    $ tracboat export --trac-uri=http://localhost/xmlrpc --format=json --out-file=myproject.json

Migrate to GitLab
~~~~~~~~~~~~~~~~~

.. code:: shell

    $ cat awesomemigration.toml
    [tracboat]
    from_export_file = "myexportedtracproject.json"
    gitlab_project_name = "migrated/myproject"
    # see below to choose the right version
    gitlab_version = "10.5"
    gitlab_db_password = "Բարեւ աշխարհ"
    $ tracboat --config-file=awesomemigration.toml migrate

GitLab version compatibility
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Not all versions of GitLab need a specific model. You can refer to the table below to choose the correct model for your GitLab version.

+----------------+---------------------------+
| Tracboat model | Compatible GitLab version |
+================+===========================+
| 11.10          | 11.10                     |
+----------------+---------------------------+
| 11.0           | 11.0, 11.1, 11.2          |
+----------------+---------------------------+
| 10.5           | 10.5, 10.6, 10.7, 10.8    |
+----------------+---------------------------+
| 10.4           | 10.4                      |
+----------------+---------------------------+
| 10.3           | 10.3                      |
+----------------+---------------------------+
| 10.2           | 10.2                      |
+----------------+---------------------------+
| 9.5            | 9.5                       |
+----------------+---------------------------+
| 9.4            | 9.4                       |
+----------------+---------------------------+
| 9.3            | 9.3                       |
+----------------+---------------------------+
| 9.0            | 9.0                       |
+----------------+---------------------------+
| 8.17           | 8.17                      |
+----------------+---------------------------+
| 8.16           | 8.16                      |
+----------------+---------------------------+
| 8.15           | 8.15                      |
+----------------+---------------------------+
| 8.13           | 8.13                      |
+----------------+---------------------------+
| 8.7            | 8.7                       |
+----------------+---------------------------+
| 8.5            | 8.5                       |
+----------------+---------------------------+
| 8.4            | 8.4                       |
+----------------+---------------------------+

If your GitLab version is not in the table, it has not been tested yet.
Try with the first model lower than your version, and report any issue you encounter.

e.g. for GitLab 9.2, try 9.0 model

Migrating users
~~~~~~~~~~~~~~~

During a migration we need to map Trac usernames to GitLab user accounts
to keep all associations between issues, changelog entries and wiki
pages and their authors. By default, all Trac usernames are mapped to a
single GitLab user, the so called *fallback user*. This way you'll end
up with a migrated project where all activity looks like it come from a
single user. Not so fancy, but definitely handy if you just care about
content. You can specify a custom fallback username with the proper
option:

.. code:: shell

    $ cat config.toml
    [tracboat]
    fallback_user = "bot@migration.gov"

As usual, the same behaviour can be obtained via command line option or
environment variable. So doing this:

.. code:: shell

    $ export TRACBOAT_FALLBACK_USER=bot@migration.gov
    $ tracboat migrate

...is the same as doing this:

.. code:: shell

    $ tracboat migrate --fallback-user=bot@migration.gov

Mapping users
^^^^^^^^^^^^^

When you want your Trac users mapped to a GitLab user (and to the
corresponding account) you need to specify a custom *user mapping*, or
an association between a Trac username and a GitLab account. You can use
a key-value section in the configuration file:

.. code:: shell

    $ cat config.toml
    [tracboat.usermap]
        tracuser1 = "gitlabuser1@foo.com"
        tracuser2 = "gitlabuser2@foo.com"
        tracuser3 = "gitlabuser1@foo.com"

In this case, every action that in the Trac project belongs to
``tracuser1``, in the migrated GitLab project will end up as being
authored by ``gitlabuser1@foo.com``.

You can add extra mappings using the ``--umap`` command line option, so
doing like this:

.. code:: shell

    $ tracboat migrate --umap tracuser1 gitlabuser1@foo.com --umap tracuser2 gitlabuser2@foo.com ...

...obtains exactly the same behaviour as with the configuration file
above. *Remember that for repeated values, command line takes precedence
over configuration file.*

Custom user attributes
^^^^^^^^^^^^^^^^^^^^^^

If a user doesn't exist in GitLab yet, he will be created during the
migration process. However, creating a new GitLab account is a fairly
complex affair: you can specify social accounts, biography, links and `a
lot of other
stuff <https://docs.gitlab.com/ce/api/users.html#user-creation>`__. If
you don't say anything about how an user should be created, Tracboat
uses some defaults. However you can throw a proper section in the
configuration file to tweak those user creation attributes:

.. code:: shell

    $ cat config.toml
    [tracboat.users.default]
        admin = false
        external = true
        website_url = "http://www.foo.gov"

Those values will be applied to *all* new accounts created during the
migration process. However, you can specify additional ``user``
subsections to precisely control which values would be used for a
particular account:

.. code:: shell

    $ cat config.toml
    [tracboat.users.default]
        admin = false
        external = true
        website_url = "http://www.foo.gov"

    [tracboat.users."theboss@foo.gov"]
        username = "theboss"
        bio = "Hi. I am the boss here."
        admin = true
        twitter = "@theboss"
        external = false

In this case, all users are going to be created with the attributes
contained in the ``[tracboat.users.default]`` section except for the
boss that asked explicitly for some extra goodies.

Example
-------

This is a fairly complete configuration example with a usermap and
custom user attributes. You can find additional examples in the
``examples/`` directory.

.. code:: ini

    # Tracboat will look for values in the [tracboat] section only, so
    # you can merge in a single file values for other applications.

    [tracboat]

    # The Trac instance to be crawled.
    # If you have any secrets in the URL (just like in this case,
    # our password is in plain text), consider using the corresponding
    # environment variable TRACBOAT_TRAC_URI to avoid having secrets in
    # the configuration file.
    trac_uri = "https://myuser:MYPASSWORD@localhost/login/xmlrpc"

    # Disable ssl certificate verification (e.g.: needed with self signed certs).
    ssl_verify = false

    # The GitLab project name.
    # Can be specified as a path, subdirectories will be treated as GitLab
    # namespaces.
    gitlab_project_name = "migrated/myproject"

    # The fallback user, used when a Trac username has no entry in the
    # [tracboat.usermap] section.
    fallback_user = "bot@tracboat.gov"

    # Users configuration.
    # Every section beyond this point can be passed in separate TOML files
    # with repeated --umap-file command line options or directly here:
    #
    # umap_file = ['users1.toml', 'users2.toml']

    # The Trac -> GitLab user conversion mapping.
    # It is *highly* recommended to use a valid email address for the GitLab part
    # since by default each account will be created with a random password
    # (you need a valid address for the password reset procedure to work properly).
    [tracboat.usermap]
        tracuser1 = "gitlabuser1@foo.com"
        tracuser2 = "gitlabuser2@foo.com"
        tracuser3 = "gitlabuser3@foo.com"
        tracuser4 = "gitlabuser4@foo.com"

    [tracboat.users]
    # GitLab users attributes.
    # This section allows to specify custom attributes
    # to be used during GitLab user creation. Accepted values are
    # listed here:
    # https://docs.gitlab.com/ce/api/users.html#user-creation

    [tracboat.users.default]
        # This 'default' section specifies attributes applied
        # to all new GitLab users.
        external = true

    [tracboat.users."gitlabuser4@foo.com"]
        # This section affects a specific user (in this case "gitlabuser4@foo.com").
        # These key-value entries will be merged with those in the
        # [tracboat.users.default] section. For repeated values, those specified
        # here will prevail.
        #
        # There are some mandatory values that must be specified
        # for each user, otherwise the following default values
        # will be used:
        #
        # username = ...
        #     Defaults to the user part of the GitLab email address
        #     (e.g. "gitlabuser4" for "gitlabuser4@foo.com").
        #
        # encrypted_password = ...
        #     Defaults to a random password (at the first login the user must carry
        #     out a password reset procedure). Anyway, you are *highly* discouraged
        #     to specify secrets here, please stick to the default behaviour.
        username = "theboss"
        bio = "Hi. I am the boss here."
        admin = true
        twitter = "@theboss"
        external = false  # this value overrides tracboat.users.default.external

    [tracboat.users."bot@tracboat.gov"]
        # This section affects the fallback user, used when a Trac
        # username has no entry in the [tracboat.usermap] section.
        username = "migration-bot"
        bio = "Hi. I am the robot that migrated all your stuff."
        admin = true
        external = false

Credits
-------

Tracboat was initially created by `Federico Ficarelli <https://github.com/nazavode>`__
and is now maintained by a pack of great contributors
(refer to ``AUTHORS`` file for details).
Initial inspiration and core migration logic comes from the
`trac-to-gitlab <https://github.com/moimael/trac-to-gitlab>`__ project
by `Maël Lavault <https://github.com/moimael>`__: this project was born
from heavy cleanup and refactoring of that original code, so this is why
this spinoff inherited its
`GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`__ license.

.. |build-status| image:: https://travis-ci.org/nazavode/tracboat.svg?branch=master
    :target: https://travis-ci.org/nazavode/tracboat
    :alt: Build status

.. |coverage-status| image:: https://codecov.io/gh/nazavode/tracboat/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/nazavode/tracboat
    :alt: Coverage report

.. |license-status| image:: https://img.shields.io/badge/License-GPL%20v3-blue.svg
    :target: http://www.gnu.org/licenses/gpl-3.0
    :alt: License

.. |codeqa| image:: https://api.codacy.com/project/badge/Grade/7c3a29688a074f91b0ce1b89f4d1f3d4
   :target: https://www.codacy.com/app/federico-ficarelli/tracboat?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=nazavode/tracboat&amp;utm_campaign=Badge_Grade
   :alt: Codacy

.. .. |pypi| image:: https://badge.fury.io/py/tracboat.svg
..     :target: https://badge.fury.io/py/tracboat
..     :alt: PyPI
