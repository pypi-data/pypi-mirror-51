|logo|


Limonado: Tornado API Tools
****************************

.. image:: https://img.shields.io/travis/ferretgo/limonado/master.svg?style=flat-square
    :target: https://travis-ci.org/ferretgo/limonado
    :alt: Travis Build Status

.. image:: https://img.shields.io/github/release/ferretgo/limonado.svg?style=flat-square
    :target: https://github.com/ferretgo/limonado/releases
    :alt: Current Release Version


.. image:: https://img.shields.io/pypi/v/limonado.svg?style=flat-square
    :target: https://pypi.python.org/pypi/limonado
    :alt: pypi Version


.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: http://limonado.readthedocs.io/en/latest/
    :alt: Documentation Version


.. image:: https://coveralls.io/repos/github/ferretgo/limonado/badge.svg?branch=master&style=flat-square
   :target: https://coveralls.io/github/ferretgo/limonado?branch=master
   :alt: Coverage


.. image:: https://img.shields.io/pypi/pyversions/limonado.svg?style=flat-square
    :target: https://github.com/ferretgo/limonado
    :alt: Python versions

.. contents ::


Introduction
------------


Dependencies
---------------------



Documentation
--------------

The latest documentation can be found at `<http://limonado.readthedocs.io/en/latest/>`_


License
-------

MIT License


Source code
-----------

* https://github.com/ferretgo/limonado/


Authors
-------

* `Andrii Gakhov @gakhov`
* `Jean Vancoppenolle @jvcop`


Install with pip
--------------------

Installation requires a working build environment.

.. code:: bash

    $ pip3 install -U limonado

When using pip it is generally recommended to install packages in a ``virtualenv``
to avoid modifying system state:

.. code:: bash

    $ virtualenv .env -p python3 --no-site-packages
    $ source .env/bin/activate
    $ pip3 install -U limonado


Compile from source
---------------------

The other way to install Limonado is to clone its
`GitHub repository <https://github.com/ferretgo/limonado>`_ and build it from
source.

.. code:: bash

    $ git clone https://github.com/ferretgo/limonado.git
    $ cd limonado

    $ make build

    $ bin/pip3 install -r requirements-dev.txt
    $ make tests


.. |logo| image:: https://raw.githubusercontent.com/ferretgo/limonado/master/docs/_static/logo.png
