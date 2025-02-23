Overview of Radiant Voices
==========================

Part of the Metrasynth_ project.

.. _Metrasynth: https://metrasynth.github.io/

Radiant Voices provides tools and an object model to
**create, read, modify, and write SunVox files**.
This includes project files ending in ``.sunvox``,
and module/synth files ending in ``.sunsynth``.


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


Support for multiple languages
------------------------------

Multiple programming languages are supported.

This is accomplished by combining a structured file format specification
with a code generation framework.

Supported languages currently include:

- Python 3.8+
- Typescript


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
