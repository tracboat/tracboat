========
TracBoat
========

A life boat to escape the Trac ocean liner.

**TracBoat** is a toolbox for exporting whole Trac instances, saving them and
migrating them to other platforms.

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

* ``Python >= 2.7`` (including ``Python 3.x``)
* `peewee <https://pypi.python.org/pypi/peewee>`_
* `psycopg2 <https://pypi.python.org/pypi/psycopg2>`_
* `six <https://pypi.python.org/pypi/six>`_
* `click <https://pypi.python.org/pypi/click>`_
* `toml <https://pypi.python.org/pypi/toml>`_
* `pymongo <https://pypi.python.org/pypi/pymongo>`_

Getting started
===============

TODO

Credits
=======

The initial inspiration and core migration logic comes from the 
`trac-to-gitlab <https://github.com/moimael/trac-to-gitlab>`_ project by
`Maël Lavault <https://github.com/moimael>`_: this project was born from
heavy cleanup and refactoring of that original code, so this is why this spinoff
inherited its `GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_ license.

Changes
=======

0.9.0 *(unreleased)*
--------------------

Added
`````
- Project import.


.. _trac:
    https://trac.edgewall.org/
