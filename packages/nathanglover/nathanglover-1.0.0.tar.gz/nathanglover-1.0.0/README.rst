========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |appveyor| |requires|
        | |codecov|
        | |landscape|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|

.. |docs| image:: https://readthedocs.org/projects/python-nathanglover/badge/?style=flat
    :target: https://readthedocs.org/projects/python-nathanglover
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/nathanglover/python-nathanglover.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/nathanglover/python-nathanglover

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/nathanglover/python-nathanglover?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/nathanglover/python-nathanglover

.. |requires| image:: https://requires.io/github/nathanglover/python-nathanglover/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/nathanglover/python-nathanglover/requirements/?branch=master

.. |codecov| image:: https://codecov.io/github/nathanglover/python-nathanglover/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/nathanglover/python-nathanglover

.. |landscape| image:: https://landscape.io/github/nathanglover/python-nathanglover/master/landscape.svg?style=flat
    :target: https://landscape.io/github/nathanglover/python-nathanglover/master
    :alt: Code Quality Status

.. |version| image:: https://img.shields.io/pypi/v/nathanglover.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/nathanglover

.. |commits-since| image:: https://img.shields.io/github/commits-since/nathanglover/python-nathanglover/v1.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/t04glovern/python-nathanglover/compare/v1.0.0...master

.. |wheel| image:: https://img.shields.io/pypi/wheel/nathanglover.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/nathanglover

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/nathanglover.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/nathanglover

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/nathanglover.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/nathanglover


.. end-badges

My Contact Details

* Free software: MIT license

Installation
============

::

    pip install nathanglover

Documentation
=============

https://python-nathanglover.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
