Introduction
============

Radiant Voices provides tools to
**create, read, modify, and write SunVox files**.
This includes project files ending in ``.sunvox``,
and module/synth files ending in ``.sunsynth`.


Data structures and APIs
------------------------

Radiant Voices aims to provide 100% coverage of
all data structures used by SunVox,
as well as object-oriented and functional means
of creating and manipulating those structures.

Using the API, you can do things not possible
with the standard SunVox interface, such as:

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


Interaction with the SunVox DLL
-------------------------------

By combining Radiant Voices with sunvox-dll-python_,
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


File format documentation
-------------------------

As there is currently no official description of the SunVox file format [#]_,
Radiant Voices serves as a *de facto* reference document and
open source implementation of the format.

..  [#] See the `"File format .sunvox" thread`_ on the official SunVox forum.

..  _"File format .sunvox" thread:
    http://www.warmplace.ru/forum/viewtopic.php?t=1943#p5562


About SunVox
------------

From the `official SunVox website`_:

    SunVox is a small, fast and powerful `modular synthesizer`_ with
    pattern-based sequencer (tracker_).
    It is a tool for those people who like to compose music wherever they are,
    whenever they wish. On any device.
    SunVox is available for Windows, OS X, Linux, Maemo, Meego, Raspberry Pi,
    Windows Mobile (WindowsCE), PalmOS, iOS and Android.

..  _official SunVox website:
    http://www.warmplace.ru/soft/sunvox/

..  _modular synthesizer:
    https://en.wikipedia.org/wiki/Modular_synthesizer

..  _tracker:
    https://en.wikipedia.org/wiki/Music_tracker
