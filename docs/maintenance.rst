===========
Maintenance
===========

This is a loose collection of notes for maintaining releases of Radiant Voices
to relevant package indexes.

Python (PyPI)
=============

Tagging a release
-----------------

::

    $ $EDITOR rv/__init__.py

        __version__ = 'x.y.z'

    $ $EDITOR CHANGELOG.rst

        (Add changelog items as needed)

    $ git add rv/__init__.py
    $ git commit -m "Prepare for x.y.z release"
    $ git tag x.y.z
    $ git push --tags

Testing using devpi
-------------------

::

    $ devpi login <username> --password=<password>
    $ devpi upload
    $ virtualenv testenv
    $ cd testenv
    $ . bin/activate
    $ devpi install radiant-voices
    $ python -c "import rv; print(rv.__version__)"
    x.y.z
    $ deactivate
    $ cd ..
    $ rm -rf testenv

Upload to PyPI
--------------

::

    $ twine upload dist/radiant-voices-x.y.z.tar.gz

JavaScript (NPM)
================

Tagging a release
-----------------

Testing
-------

Upload to npm
-------------
