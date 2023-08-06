===========================
Scalingo PostgresSQL dumper
===========================


.. image:: https://img.shields.io/pypi/v/scalpg_dump.svg
        :target: https://pypi.python.org/pypi/scalpg_dump

.. image:: https://img.shields.io/travis/tobiase/scalpg_dump.svg
        :target: https://travis-ci.org/tobiase/scalpg_dump

.. image:: https://readthedocs.org/projects/scalpg-dump/badge/?version=latest
        :target: https://scalpg-dump.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/tobiase/scalpg_dump/shield.svg
     :target: https://pyup.io/repos/github/tobiase/scalpg_dump/
     :alt: Updates


Dumps your Scalingo PostgreSQL database without the hustle

To dump the database go to a local directory that's associated with a Scalingo app

Scalingo PostgresSQL dumper requires a working installation of the Scalingo CLI
Install Scalingo CLI: http://doc.scalingo.com/app/command-line-tool.html

* Free software: MIT license
* Documentation: https://scalpg-dump.readthedocs.io.


Usage
-----

Dump to file::

    scalpg_dump > dump.sql

Pass version to scalingos dbclient-fetcher::

    scalpg_dump -v11

Run for specific version / region::

    SCALINGO_APP=your-app SCALINGO_REGION=agora-fr1 scalpg_dump



Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

