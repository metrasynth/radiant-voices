Overview of Radiant Voices
==========================

..  start-badges

|buildstatus| |docs|

..  end-badges

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/


Create, modify, read, and write SunVox files
--------------------------------------------

..  uml::

    @startuml
    rectangle "Python Interpreter" as python {
        rectangle "<your_app>" as app {
            rectangle "Radiant Voices\nobject model" as obj
        }
        rectangle "Radiant Voices\nPython package" as rv
    }
    rectangle "SunVox file\nor buffer" as file
    rv <-up-> obj
    rv <-down-> file
    @enduml


Data structures
---------------

Radiant Voices provides:

- A set of data structures covering nearly 100% of the SunVox file format.

- "Pythonic" API for creating and manipulating those structures.


Read SunVox files
-----------------

The ``.sunvox`` and ``.sunsynth`` file formats use the `IFF`_ container format.

..  _IFF:
    https://en.wikipedia.org/wiki/Interchange_File_Format

Radiant Voices leverages Python's :py:mod:`chunk` module to read that format
and translate it to in-memory data structures.


Write SunVox files
------------------

Once structures are ready to play, Radiant Voices can write
to a file or buffer using the ``.sunvox`` or ``.sunsynth`` format.


Document the SunVox file format
-------------------------------

Radiant Voices intends to serve as a *de facto* source of documentation
about the format, as there is currently `no official documentation for the
SunVox file format <http://www.warmplace.ru/forum/viewtopic.php?t=1943#p5562>`__.

The interpretation of SunVox file formats is based on a mix of "clean room"
style inspection of what SunVox writes to disk when a file is edited
a specific way, as well as the `most recent BSD-licensed source code
for the SunVox audio engine <https://github.com/warmplace/sunvox_sources>`__.


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
    $ wget http://www.warmplace.ru/soft/sunvox/sunvox_dll.zip
    $ unzip sunvox_dll.zip
    $ export SUNVOX_DLL_BASE=$PWD/sunvox_dll
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
