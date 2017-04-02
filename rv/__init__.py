"""
Top-level module, exposing the most common functionality of Radiant Voices.

When you ``import rv``, you'll be able to access the following
classes, functions, and objects, without needing any other import statements:

-   ``rv.Note``: represents notes within a pattern
    (see :py:class:`rv.note.Note`)

-   ``rv.NOTE``: all notes available for patterns or mappings
    (see :py:class:`rv.note.NOTE`)

-   ``rv.NOTECMD``: all notes and note commands available for patterns
    (see :py:class:`rv.note.NOTECMD`)

-   ``rv.Pattern``: represents a pattern
    (see :py:class:`rv.pattern.Pattern`)

-   ``rv.PatternClone``: represents a clone of a pattern
    (see :py:class:`rv.pattern.PatternClone`)

-   ``rv.Project``: a SunVox project that can be read from or written to a
    ``.sunvox`` file (see :py:class:`rv.project.Project`)

-   ``rv.read_sunvox_file``: function to read a ``.sunvox`` or ``.sunsynth``
    file (see :py:func:`rv.readers.reader.read_sunvox_file`)

-   ``rv.Synth``: a SunVox synth that can be read from or written to
    a ``.sunsynth`` file (see :py:class:`rv.synth.Synth`)

-   :py:mod:`rv.modules`: classes for all SunVox module types
"""


__version__ = '0.2.0'

ENCODING = 'cp1251'
"""
Encoding used to convert 8-bit strings to/from Unicode strings.

SunVox uses the ``cp1251`` encoding which supports both US ASCII
and Cyrillic scripts.

See also `<https://en.wikipedia.org/wiki/Windows-1251>`__.
"""
