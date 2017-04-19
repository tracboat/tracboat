Requirements
============

.. Author: Federico Ficarelli
           nazavode.github.io

Until `PEP 518`_ and `Pipfile`_ become reality, requirements management must be
done with care.

What is this stuff?
-------------------

* Each ``<env>.txt`` file in this directory is a pip requirement file
  that represents a **reproducible environment**;
* each ``extra-<feature>.txt`` file in this directory is a pip requirement
  file that represents an **optional package feature** and lists all the
  dependencies needed to have it working properly;
* all of these files are't maintained directly: they must be built using
  ``pip-compile`` (from `pip-tools`_);
* sources for requirements files are in ``./src``: these are the files
  to be edited in order to apply changes to the environments.

If you need to modify requirements please have a look to
`pip-tools`_ before making any change.

.. warning:: Ubuntu bug breaks the packaging workflow.
    A severe bug in ubuntu is breaking a lot of Python packaging
    best-practices, so if you are working on it please pay extreme
    attention and:

    * avoid using ``pip-sync`` since it is currently broken;
    * be sure that the buggy dependency ``pkg-resources==0.0.0``
      injected by the ubuntu-provided ``pip`` isn't inserted in
      requirements files produced by ``pip-compile``, otherwise
      **everything would break**.

    For further details please refer to:
    https://bugs.launchpad.net/ubuntu/+source/python-pip/+bug/1635463

Environments
------------

* ``dist.txt``: package distribution and deployment;
* ``develop.txt``: development activities (running tests, ensure qa,
  bump a version, etc...);

.. _pip-tools: https://github.com/nvie/pip-tools
.. _PEP 518: https://www.python.org/dev/peps/pep-0518/
.. _Pipfile: https://github.com/pypa/pipfile
