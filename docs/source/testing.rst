Testing
=======

.. toctree::

In order to test, you must place a kismet sqlite log file at
``tests/assets/testdata.kismet_4`` and ``tests/assets/testdata.kismet_5``,
which are version 4 and version 5 log files, respectively.

Testing happens in a Docker build process:

Testing for Python 2.7:

``docker build .``

Testing for Python 3.6:

``docker build --build-arg PY_VER=3.6 .``

Testing for Python 3.7:

``docker build --build-arg PY_VER=3.7 .``
