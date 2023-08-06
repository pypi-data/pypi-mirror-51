lib_regexp
==========

|Pypi Status| |license| |maintenance|

|Build Status| |Codecov Status| |Better Code| |code climate| |snyk security|

.. |license| image:: https://img.shields.io/github/license/webcomics/pywine.svg
   :target: http://en.wikipedia.org/wiki/MIT_License
.. |maintenance| image:: https://img.shields.io/maintenance/yes/2019.svg
.. |Build Status| image:: https://travis-ci.org/bitranox/lib_regexp.svg?branch=master
   :target: https://travis-ci.org/bitranox/lib_regexp
.. for the pypi status link note the dashes, not the underscore !
.. |Pypi Status| image:: https://badge.fury.io/py/lib-regexp.svg
   :target: https://badge.fury.io/py/lib_regexp
.. |Codecov Status| image:: https://codecov.io/gh/bitranox/lib_regexp/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/bitranox/lib_regexp
.. |Better Code| image:: https://bettercodehub.com/edge/badge/bitranox/lib_regexp?branch=master
   :target: https://bettercodehub.com/results/bitranox/lib_regexp
.. |snyk security| image:: https://snyk.io/test/github/bitranox/lib_regexp/badge.svg
   :target: https://snyk.io/test/github/bitranox/lib_regexp
.. |code climate| image:: https://api.codeclimate.com/v1/badges/d854dda63a0f89c04032/maintainability
   :target: https://codeclimate.com/github/bitranox/lib_regexp/maintainability
   :alt: Maintainability

some convenience functions for regexp

supports python 3.7 and possibly other dialects.

`100% code coverage <https://codecov.io/gh/bitranox/lib_regexp>`_, mypy static type checking, tested under `Linux, OsX, Windows and Wine <https://travis-ci.org/bitranox/lib_regexp>`_, automatic daily builds  and monitoring

----

- `Installation and Upgrade`_
- `Basic Usage`_
- `Requirements`_
- `Acknowledgements`_
- `Contribute`_
- `Report Issues <https://github.com/bitranox/lib_regexp/blob/master/ISSUE_TEMPLATE.md>`_
- `Pull Request <https://github.com/bitranox/lib_regexp/blob/master/PULL_REQUEST_TEMPLATE.md>`_
- `Code of Conduct <https://github.com/bitranox/lib_regexp/blob/master/CODE_OF_CONDUCT.md>`_
- `License`_
- `Changelog`_

----

Installation and Upgrade
------------------------

From source code:

.. code-block:: bash

    # normal install
    python setup.py install
    # test without installing
    python setup.py test

via pip latest Release:

.. code-block:: bash

    # latest Release from pypi
    pip install lib_regexp

    # test without installing
    pip install lib_regexp --install-option test

via pip latest Development Version:

.. code-block:: bash

    # upgrade all dependencies regardless of version number (PREFERRED)
    pip install --upgrade git+https://github.com/bitranox/lib_regexp.git --upgrade-strategy eager
    # normal install
    pip install --upgrade git+https://github.com/bitranox/lib_regexp.git
    # test without installing
    pip install git+https://github.com/bitranox/lib_regexp.git --install-option test

via requirements.txt:

.. code-block:: bash

    # Insert following line in Your requirements.txt:
    # for the latest Release:
    lib_regexp
    # for the latest Development Version :
    git+https://github.com/bitranox/lib_regexp.git

    # to install and upgrade all modules mentioned in requirements.txt:
    pip install --upgrade -r /<path>/requirements.txt

via python:

.. code-block:: python

    # for the latest Release
    python -m pip install upgrade lib_regexp

    # for the latest Development Version
    python -m pip install upgrade git+https://github.com/bitranox/lib_regexp.git

Basic Usage
-----------

TBA

Requirements
------------
following modules will be automatically installed :

.. code-block:: bash

    ## Test Requirements
    ## following Requirements will be installed temporarily for
    ## "setup.py install test" or "pip install <package> --install-option test"
    typing ; python_version < "3.5"
    pathlib; python_version < "3.4"
    mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"
    pytest
    pytest-pep8 ; python_version < "3.5"
    pytest-codestyle ; python_version >= "3.5"
    pytest-mypy ; platform_python_implementation != "PyPy" and python_version >= "3.5"
    pytest-runner

    ## Project Requirements

Acknowledgements
----------------

- special thanks to "uncle bob" Robert C. Martin, especially for his books on "clean code" and "clean architecture"

Contribute
----------

I would love for you to fork and send me pull request for this project.
- `please Contribute <https://github.com/bitranox/lib_regexp/blob/master/CONTRIBUTING.md>`_

License
-------

This software is licensed under the `MIT license <http://en.wikipedia.org/wiki/MIT_License>`_

---

Changelog
=========

0.0.1
-----
2019-09-03: Initial public release

