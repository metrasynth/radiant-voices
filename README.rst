Overview of Radiant Voices
==========================

..  start-badges

|buildstatus| |docs|

.. |buildstatus| image:: https://img.shields.io/travis/metrasynth/radiant-voices.svg?style=flat
    :alt: build status
    :scale: 100%
    :target: https://travis-ci.org/metrasynth/radiant-voices

.. |docs| image:: https://readthedocs.org/projects/radiant-voices/badge/?version=latest
    :alt: Documentation Status
    :scale: 100%
    :target: https://radiant-voices.readthedocs.io/en/latest/?badge=latest

..  end-badges

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/

Radiant Voices provides tools to
**create, read, modify, and write SunVox files**.
This includes project files ending in ``.sunvox``,
and module/synth files ending in ``.sunsynth``.

..  uml::

    @startuml
    rectangle "Your Preferred Programming Language" as lang {
        rectangle "Your App" as app {
            rectangle "Radiant Voices\nobject model" as obj
        }
        rectangle "Radiant Voices\nPython package" as rv
    }
    rectangle "SunVox file\nor buffer" as file
    rv <-up-> obj
    rv <-down-> file
    @enduml


SunVox data structures and APIs
-------------------------------

Radiant Voices strives toward 100% coverage of
all data structures used by SunVox files,
exposing APIs for creating and manipulating those structures.

Using these APIs, you can do things not possible
with the standard SunVox interface or the SunVox DLL, such as:

- `algorithmic composition`_
- parametric synth/module design
- structure and complexity analysis
- automatic `graph layout`_ of modules
- and more...

Our collective imagination is the limit!

..  _algorithmic composition:
    https://en.wikipedia.org/wiki/Algorithmic_composition

..  _graph layout:
    https://en.wikipedia.org/wiki/Graph_drawing


Multiple languages and data access patterns
-------------------------------------------

Multiple programming languages are supported,
and in some languages both mutable and immutable APIs are provided.

This is accomplished by combining a structured file format specification
with a code generation framework.

Here are the platforms targeted by Radiant Voices:

==============  ==============  ============  ==================================
Language        Data Access     Status        Notes
==============  ==============  ============  ==================================
Python 3.8      mutable         Not started
Python 3.8      immutable       Not started   Using Pyrsistent_
TypeScript      mutable         Not started
TypeScript      immutable       Not started   Using immer_
Pixilang        mutable         Not started
==============  ==============  ============  ==================================

..  _Pyrsistent:
    https://github.com/tobgu/pyrsistent

..  _immer:
    https://github.com/immerjs/immer

Mutable data access means that you directly manipulate objects
that represent a SunVox data structure.
Code written this way may be easier to read and write.

Immutable data access lets you keep pointers
to previous versions of data structures.
Changes are made by efficiently constructing a new version
of the entire data structure.
Code written this way may take more practice to read and write,
but is useful for certain kinds of tools that could benefit from
efficient undo/redo.


Interaction with the SunVox DLL
-------------------------------

By combining Radiant Voices with sunvox-dll-python_ for Python
(or the SunVox library wrapper for your language),
one can also create alternative editing and performance tools
to use alongside, or instead of, the official SunVox app.

The two packages work together to provide convenient high-level
APIs for loading project and module objects directly into
playback slots managed by the SunVox DLL.

Some possibilities might include:

- alternative project editors
- generative_ sound design using `genetic algorithms`_
- network-enabled performance tools

What can *you* come up with?

..  _sunvox-dll-python:
    https://sunvox-dll-python.readthedocs.io/

..  _generative:
    https://en.wikipedia.org/wiki/Generative_Design

..  _genetic algorithms:
    https://en.wikipedia.org/wiki/Genetic_algorithm


SunVox file format documentation
--------------------------------

Radiant Voices intends to serve as a *de facto* source of documentation
about the format, as there is currently `no official documentation for the
SunVox file format <http://www.warmplace.ru/forum/viewtopic.php?t=1943#p5562>`__.

The interpretation of SunVox file formats is based on a mix of "clean room"
style inspection of what SunVox writes to disk when a file is edited
a specific way, the `most recent BSD-licensed source code
for the SunVox audio engine <https://github.com/warmplace/sunvox_sources>`__,
and consultation with NightRadio (the author of SunVox).

Documentation is provided in the form of prose in the English language,
as well as a specification defined in YAML format.


Requirements
------------

- A supported programming language.

- OS and platform supported by `sunvox-dll-python`_, if working with
  the native SunVox DLL.


About SunVox
------------

From the `SunVox home page`_:

    SunVox is a small, fast and powerful modular synthesizer with pattern-based sequencer (tracker).
    It is a tool for those people who like to compose music wherever they are, whenever they wish.
    On any device. SunVox is available for Windows, OS X, Linux, Maemo, Meego, Raspberry Pi,
    Windows Mobile (WindowsCE), PalmOS, iOS and Android.

.. _SunVox home page: http://www.warmplace.ru/soft/sunvox/
