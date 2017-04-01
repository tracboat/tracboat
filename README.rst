.. image:: https://nazavode.github.io/img/lifeboat-banner.png

========
TracBoat
========

A life boat to escape the Trac ocean liner.

**TracBoat** is a toolbox for exporting whole Trac instances, saving them and
migrating them to other platforms.

Features
========

* Export Trac projects along with issues, issue changelogs (with attachments)
  and wiki pages (with attachments)
* Export Trac projects to local files (in json, toml, Python literal or Python
  pickle formats)
* Migrate Trac projects directly from remote instances as well as from previously
  created export files
* Migrate Trac projects to a live GitLab instance
* Migrate Trac projects to a mocked GitLab on the file system to check
  for correctness

Installation
============
TracBoat is available on `pypi <https://pypi.python.org/pypi/tracboat>`_,
so to install it just type:

.. code::

    $ pip install tracboat

If you want to **install from source**, doing it in a ``virtualenv`` is *highly
recommended*. After having this repo cloned, just type:

.. code::

    $ cd tracboat
    $ virtualenv -p python2.7 VENV
    $ source VENV/bin/activate
    $ pip install -r requirements.txt
    $ pip install -e .


Dependencies
============

* Python >= 2.7 or Python 3.x
* `peewee <https://pypi.python.org/pypi/peewee>`_
* `psycopg2 <https://pypi.python.org/pypi/psycopg2>`_
* `six <https://pypi.python.org/pypi/six>`_
* `click <https://pypi.python.org/pypi/click>`_
* `toml <https://pypi.python.org/pypi/toml>`_
* `pymongo <https://pypi.python.org/pypi/pymongo>`_

Getting started
===============

Every command line option can be specified as an evironment variable, so the
following command:

.. code::

    $ tracboat users --trac-uri=https://mytrac/xmlrpc --no-ssl-verify

...is exactly the same as the following:

.. code::

    $ export TRACBOAT_TRAC_URI=https://mytrac/xmlrpc
    $ export TRACBOAT_SSL_VERIFY=0
    $ tracboat users

Another way to conveniently configure ``tracboat`` is with a configuration file
in `TOML <https://github.com/toml-lang/toml>`_ format. Providing a file

.. code::

    $ cat mytrac.toml
    [tracboat]
    trac_uri = "https://mytrac/xmlrpc"
    ssl_verify = false
    $ tracboat --config-file=mytrac.toml users

Please note that when a value is specified more that once, the priority order
considered is the following:

1. command line option;
2. environment variable;
3. configuration file;
4. default value.

If you are *very* curious about how to play with command line options, have a
look to the `click documentation <http://click.pocoo.org/>`_.

Collecting Trac users
---------------------

.. code::

    $ tracboat users --trac-uri=http://localhost/xmlrpc

Export a Trac instance
----------------------

.. code::

    $ tracboat export --trac-uri=http://localhost/xmlrpc --format=json --out-file=myproject.json

Migrate to GitLab
-----------------

.. code::

    $ cat awesomemigration.toml
    [tracboat]
    from-export-file = "myexportedtracproject.json"
    gitlab-project-name = "migrated/myproject"
    gitlab-version = "9.0.0"
    gitlab_db_password = "Բարեւ աշխարհ"
    $ tracboat --config-file=awesomemigration.toml migrate

Credits
=======

The initial inspiration and core migration logic comes from the
`trac-to-gitlab <https://github.com/moimael/trac-to-gitlab>`_ project by
`Maël Lavault <https://github.com/moimael>`_: this project was born from
heavy cleanup and refactoring of that original code, so this is why this spinoff
inherited its `GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_ license.

Changes
=======

0.1.0 *(unreleased)*
--------------------

Added
`````
- Project import.


.. _trac:
    https://trac.edgewall.org/
