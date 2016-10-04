Radiant Voices
==============

|buildstatus| |docs|

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/


Purpose
-------

Create, modify, read, and write SunVox files.


Requirements
------------

- Python 3.5


Quick start
-----------

The "hello world" example will construct a SunVox project in memory
containing a FM module connected to the Output module.
It will then load it into the SunVox DLL and send a note-on command to the
FM module::

    $ git clone https://github.com/metrasynth/radiant-voices
    $ git clone https://github.com/metrasynth/sunvox-dll-python
    $ pip install -e sunvox-dll-python
    $ pip install -e radiant-voices
    $ cd radiant-voices/examples
    $ python helloworld.py


.. |buildstatus| image:: https://img.shields.io/travis/metrasynth/radiant-voices.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/metrasynth/radiant-voices

.. |docs| image:: https://readthedocs.org/projects/radiant-voices/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://radiant-voices.readthedocs.io/en/latest/?badge=latest
