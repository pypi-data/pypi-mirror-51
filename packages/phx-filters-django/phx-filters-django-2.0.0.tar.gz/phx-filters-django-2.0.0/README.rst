.. image:: https://travis-ci.org/todofixthis/filters-django.svg?branch=master
   :target: https://travis-ci.org/todofixthis/filters-django
.. image:: https://readthedocs.org/projects/filters/badge/?version=latest
   :target: http://filters.readthedocs.io/

Django Filters
==============
Adds filters for for Django-specific features, including:

- Search for a DB model instance matching the incoming value.


Minimum Requirements
--------------------
These filters are compatible with Django v2.x.

If you encounter any issues, please report them on our `Bug Tracker`_, and be
sure to indicate which version of Django you are using.


Installation
------------
This package is an extension for the `Filters library`, so you can install it
as an extra to ``phx-filters``:

.. code:: bash

   pip install phx-filters[django]


If desired, you can install this package separately.  This allows you to control
the package version separately from ``phx-filters``.

.. code:: bash

   pip install phx-filters-django


Running Unit Tests
------------------
To run unit tests after installing from source::

  pip install -e .[test-runner]
  python manage.py test

This project is also compatible with `tox`_, which will run the unit tests in
different virtual environments (one for each supported version of Python).

Install the package with the ``test-runner`` extra to set up the necessary
dependencies, and then you can run the tests with the ``tox`` command::

  pip install -e .[test-runner]
  tox -p all


.. _Bug Tracker: https://github.com/eflglobal/filters-django/issues
.. _Filters library: https://pypi.python.org/pypi/filters
.. _tox: https://tox.readthedocs.io/
