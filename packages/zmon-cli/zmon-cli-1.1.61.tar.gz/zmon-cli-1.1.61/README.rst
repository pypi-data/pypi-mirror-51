========
ZMON CLI
========

.. image:: https://travis-ci.org/zalando-zmon/zmon-cli.svg?branch=master
   :target: https://travis-ci.org/zalando-zmon/zmon-cli
   :alt: Build Status

.. image:: https://img.shields.io/codecov/c/github/zalando-zmon/zmon-cli.svg?maxAge=2592000
   :target: https://codecov.io/gh/zalando-zmon/zmon-cli
   :alt: Code Coverage

.. image:: https://img.shields.io/pypi/dw/zmon-cli.svg
   :target: https://pypi.python.org/pypi/zmon-cli/
   :alt: PyPI Downloads

.. image:: https://img.shields.io/pypi/v/zmon-cli.svg
   :target: https://pypi.python.org/pypi/zmon-cli/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/l/zmon-cli.svg
   :target: https://pypi.python.org/pypi/zmon-cli/
   :alt: License

Command line client for the Zalando Monitoring solution (ZMON).

Requires Python 3.4+

Installation
============

.. code-block:: bash

    $ sudo pip3 install --upgrade zmon-cli

Documentation
=============

  http://zmon.readthedocs.org/en/latest/developer/zmon-cli.html

Example
=======

Creating or updating a single check definition from its YAML file:

.. code-block:: bash

    $ zmon check-definitions update examples/check-definitions/zmon-stale-active-alerts.yaml
