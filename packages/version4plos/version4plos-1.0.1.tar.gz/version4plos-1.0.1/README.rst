About
=====

Console app and Python API for automated tracking of `PLOS LaTeX template`_
versions.

Please cite this project in your papers::

    @misc{version4plos,
      title={{version4plos public code repository}},
      author={Mari{\'c}, Petar},
      year={2019},
      url={https://github.com/petarmaric/version4plos},
    }

.. _`PLOS LaTeX template`: https://journals.plos.org/plosone/s/latex

Installation
============

To install version4plos run::

    $ pip install version4plos

Console app usage
=================

Quick start::

    $ version4plos

Show help::

    $ version4plos --help

Python API usage
================

Quick start::

    >>> import logging
    >>> logging.basicConfig(level=logging.DEBUG, format="[%(levelname)s] %(message)s")

    >>> from version4plos import get_template_version
    >>> get_template_version()

Contribute
==========

If you find any bugs, or wish to propose new features `please let us know`_.

If you'd like to contribute, simply fork `the repository`_, commit your changes
and send a pull request. Make sure you add yourself to `AUTHORS`_.

.. _`please let us know`: https://github.com/petarmaric/version4plos/issues/new
.. _`the repository`: https://github.com/petarmaric/version4plos
.. _`AUTHORS`: https://github.com/petarmaric/version4plos/blob/master/AUTHORS
