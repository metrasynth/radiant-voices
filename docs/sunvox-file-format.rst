SunVox File Format
==================

This document is an ongoing effort to describe the SunVox file format
in a way that is useful to developers of Radiant Voices
(and other apps that want to read/write SunVox files).

Little-endian
-------------

Multi-byte integer values are always encoded in little-endian format.

IFF-style containers
--------------------

All SunVox files use a variation of the `Interchange File Format`_.

Each file is a stream of chunks.

Each chunk consists of a 4-byte ASCII string known as a "Type ID",
then a unsigned int32 known as the "Length",
and finally a blob of that length (if length was not 0).

Some chunks are specified as being containers themselves,
such as when a SunVox project is embedded within a MetaModule.
In this case, the length of the outer chunk is for the entire project data.
Then, the data is parsed as a separate container.

..  _Interchange File Format:
    https://en.wikipedia.org/wiki/Interchange_File_Format

..  note::

    You can use Radiant Voices to inspect the IFF structure
    of a SunVox file::

        $ python -m rv.lib.iff myproject.sunvox

        SVOX

        VERS  00000000: 00 03 09 01                                       ....

        BVER  00000000: 00 02 09 01                                       ....

        BPM   00000000: 7D 00 00 00                                       }...

        [ ... ]

String encoding
---------------

Whenever a human-readable string is encoded,
the `Windows-1251`_ code page is used.
It encodes Cyrillic script after the ASCII characters.

..  _Windows-1251:
    https://en.wikipedia.org/wiki/Windows-1251

File extensions
---------------

sunvox
......

Contains an entire SunVox project, with chunks in this order:

1.  Empty chunk of type ``SVOX``.

2.  `Project chunks`_.

3.  `Pattern chunks`_ for each pattern.

4.  `Module chunks`_ for each module.

sunsynth
........

Contains a single SunVox module, with chunks in this order:

1.  Empty chunk of type ``SSYN``.

2.  File format version identifier: ``VERS`` type, length 4,
    unsigned int32 value of 0x00000001.

3.  `Module chunks`_.

sunpat
......

Used by SunVox for copying and pasting selections of pattern data
in the pattern editor, via the ``.sunvox_clipboard.sunpat`` file.

Contains a selection of pattern data, encoded in a single ``SVOX`` chunk.

The chunk contents are as follows:

======  ====================  ===================================================
Offset  Type                  Purpose
======  ====================  ===================================================
0x00    unsigned int32        Number of tracks in pattern
0x04    unsigned int32        Number of lines in pattern
0x08    note[lines][tracks]   2-D array of notes_
======  ====================  ===================================================

sunpats
.......

Used by SunVox for copying and pasting patterns in the timeline,
via the ``.sunvox_clipboard.sunpats`` file.

Contains multiple patterns, with chunks in this order:

1.  Empty chunk of type ``SVOX``.

2.  `Project chunks`_ for the project that the patterns were copied from.

3.  `Pattern chunks`_ for each pattern.

Project chunks
--------------

========  ================  =======================================================
Type ID   Format            Purpose
========  ================  =======================================================
``VERS``  byte[4]           SunVox version (LSB to MSB, e.g. 00020901 for v1.9.2.0)
``BVER``  byte[4]           Based-on version
``BPM ``  unsigned int32    Initial BPM (beats per minute)
``SPED``  unsigned int32    Initial TPL (ticks per line)
``TGRD``  unsigned int32    Time grid (number of lines per "beat")
``TGD2``  unsigned int32    Time grid 2 (number of "beats" per "measure")
``GVOL``  unsigned int32    Global volume
``NAME``  cstring           Project name
``MSCL``  unsigned int32    Modules scale
``MZOO``  unsigned int32    Modules zoom
``MXOF``  signed int32      Modules X offset
``MYOF``  signed int32      Modules Y offset
``LMSK``  unsigned int32    `Modules layer mask`_
``CURL``  unsigned int32    Modules current layer (0 to 7)
``TIME``  signed int32      Current timeline position
``SELS``  unsigned int32    Selected module index
``LGEN``  unsigned int32    Unknown purpose - always has value 0x00000001
``PATN``  unsigned int32    Pattern cursor: index of pattern being edited
``PATT``  unsigned int32    Pattern cursor: track index
``PATL``  unsigned int32    Pattern cursor: line index
========  ================  =======================================================

Modules layer mask
..................

The first byte of this value is a bitmask of layers visible in the modules.
When a bit is on, the corresponding layer will always be visible
regardless of whether that layer is the current layer.

Pattern chunks
--------------

If a pattern doesn't exist at a given index,
the only chunk present will be ``PEND``.

Patterns
........

========  ====================  =======================================================
Type ID   Format                Purpose
========  ====================  =======================================================
``PDTA``  note[lines][tracks]   2-D array of notes_
``PNME``  cstring               Pattern name (optional)
``PCHN``  unsigned int32        Number of tracks in pattern
``PLIN``  unsigned int32        Number of lines in pattern
``PYSZ``  unsigned int32        Height of pattern in timeline
``PFLG``  bitmap (4 bytes)      `Pattern appearance flags`_
``PICO``  bitmap (32 bytes)     Pattern icon (16×16 bitmap, with top-left origin)
``PFGC``  unsigned int8[3]      Foreground color (RGB)
``PBGC``  unsigned int8[3]      Background color (RGB)
``PFFF``  bitmap (4 bytes)      `Pattern flags`_
``PXXX``  signed int32          X position in timeline
``PYYY``  signed int32          Y position in timeline
========  ====================  =======================================================

Pattern clones
..............

========  ====================  =======================================================
Type ID   Format                Purpose
========  ====================  =======================================================
``PPAR``  unsigned int32        Index of source pattern
``PFFF``  bitmap (4 bytes)      `Pattern flags`_
``PXXX``  signed int32          X position in timeline
``PYYY``  signed int32          Y position in timeline
========  ====================  =======================================================

Notes
.....

Each note is an 8-byte structure:

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    byte              NOTECMD_ number
0x01    unsigned int8     Velocity (0x00 = empty, 0x01 = silent, 0x81 = max)
0x02    unsigned int8     Module index (0x00 = empty)
0x03    zero byte         Reserved
0x04    unsigned int8     Controller
0x05    unsigned int8     Effect
0x06    unsigned int16    XXYY value
0x06    unsigned int8     XX value
0x07    unsigned int8     YY value
======  ================  ===================================================

NOTECMD
.......

======  ======================
Value   Purpose
======  ======================
0x00    Empty
0x01    C-0
 ...     ...
0x79    B-9
0x80    Note off
0x85    Set pitch
0x86    Effect previous track
======  ======================

Pattern appearance flags
........................

(To be documented)

Pattern flags
.............

(To be documented)

Module chunks
-------------

If a module doesn't exist at a given index,
the only chunk present will be ``SEND``.

========  ====================  =======================================================
Type ID   Format                Purpose
========  ====================  =======================================================
``SFFF``  bitmap (4 bytes)      `Module flags`_
``SNAM``  string[32]            Module name (zero-padded)
``STYP``  cstring               Module type (not present for "Output" module)
``SFIN``  signed int32          Finetune
``SREL``  signed int32          Relative note
``SXXX``  signed int32          X position (not in sunsynth files)
``SYYY``  signed int32          Y position (not in sunsynth files)
``SZZZ``  signed int32          Layer (not in sunsynth files)
``SSCL``  unsigned int32        Scale
``SVPR``  bitmap (4 bytes)      `Module visualization flags`_ (not in sunsynth files)
``SCOL``  bytes[3]              Color (RGB)
``SMII``  unsigned int32        `MIDI in`_
``SMIN``  cstring               MIDI Out name (not present if none selected)
``SMIC``  unsigned int32        MIDI Out channel (0 for all channels)
``SMIB``  signed int32          MIDI Out bank (-1 for none)
``SMIP``  signed int32          MIDI Out program (-1 for none)
``SLNK``  signed int32[n]       Module indexes of incoming links, terminated with -1
``CVAL``  unsigned int32        Controller value for controller 1
 ...       ...                   ...
``CVAL``  unsigned int32        Controller value for controller *n*
``CMID``  bytes[8]              `Controller MIDI mappings`_ for controller 1
 ...       ...                   ...
``CMID``  bytes[8]              `Controller MIDI mappings`_ for controller *n*
``CHNK``  unsigned int32        `CHNK value`_ for the module, if applicable
multiple                        `Module-specific chunks`_, if applicable
========  ====================  =======================================================

Module flags
............

(To be documented)

Module visualization flags
..........................

(To be documented)

MIDI in
.......

The first bit is a flag:

======  ==========================
Value   Purpose
======  ==========================
0       MIDI In only when selected
1       MIDI In always
======  ==========================

The remaining bits are the MIDI channel the module will respond to,
shifted left by 1 bit, or 0 if it should respond to all channels
that SunVox is globally listening to.

Controller MIDI mappings
........................

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    byte              `MIDI message type`_
0x01    unsigned int8     Channel (0 for all channels)
0x02    byte              `MIDI mapping slope`_
0x03    zero byte         Reserved
0x04    unsigned int16    Message parameter
0x06    zero byte         Reserved
0x07    unsigned int8     0xff if message type is unset; 0xc8 if other value
======  ================  ===================================================

MIDI message type
.................

======  ==========================
Value   Purpose
======  ==========================
0       Unset
1       Note
2       Key Pressure
3       Control Change
4       NRPN
5       RPN
6       Program Change
7       Channel Pressure
8       Pitch Bend
======  ==========================

MIDI mapping slope
..................

======  ==========================
Value   Purpose
======  ==========================
0       Linear
1       Exp. 1
2       Exp. 2
3       S-Curve
4       Cut
5       Toggle
======  ==========================

CHNK value
..........

================  =========================================
Module type       Value
================  =========================================
Analog Generator  0x10
Generator         0x10
MetaModule        0x08 + number of user defined controllers
MultiCtl          0x10
MultiSynth        0x10
Sampler           0x0102
Sound2Ctl         0x10
SpectraVoice      0x10
Vorbis player     0x10
WaveShaper        0x10
================  =========================================

Module-specific chunks
----------------------

General format
..............

========  ====================  =======================================================
Type ID   Format                Purpose
========  ====================  =======================================================
``CHNM``  unsigned int32        Module-specific chunk number
``CHDT``  (module-dependent)    Module-specific chunk data
``CHFF``  bitmap (4 bytes)      `Chunk audio format bitmap`_
``CHFR``  unsigned int32        Chunk audio frame rate
========  ====================  =======================================================

Chunk audio format bitmap
.........................

The first 3 bits specify the format, and the 4th bit is a stereo flag:

=====   =================   ======
Value   Format              Stereo
=====   =================   ======
0x01    8-bit signed int    No
0x02    16-bit signed int   No
0x04    32-bit float        No
0x09    8-bit signed int    Yes
0x0a    16-bit signed int   Yes
0x0c    32-bit float        Yes
=====   =================   ======

Options chunks
--------------

Modules that have options store them as an array of boolean bytes
in a module-specific CHNM number, padded with zeros to 64 bytes.

Most options are flags.
The default is *off*, represented by 0x00,
and the alternative is *on*, represented by 0x01.

Some options are inverted.
The default is *on*, represented by 0x00,
and the alternative is *off*, represented by 0x01.

Some options are integers.

==================  =========================================
Module type         Options CHNM number
==================  =========================================
Analog Generator    0x01
MetaModule          0x02
MultiSynth          0x01
Sampler             0x0101
Sound2Ctl           0x00
==================  =========================================

Analog Generator options
........................

======  ========  ========================================
Offset  Type      Purpose
======  ========  ========================================
0x00    flag      Volume envelope scaling per key
0x01    flag      Filter envelope scaling per key
0x02    flag      Volume scaling per key
0x03    flag      Filter frequency scaling per key
0x04    flag      Velocity dependent filter frequency
0x05    flag      Frequency / 2
0x06    inverted  Smooth frequency change
0x07    flag      Filter frequency scaling per key reverse
0x08    flag      Retain phase
0x09    flag      Random phase
0x0a    flag      Filter frequency equals note frequency
0x0b    flag      Velocity dependent filter resonance
======  ========  ========================================

MetaModule options
..................

======  ========  ============================================
Offset  Type      Purpose
======  ========  ============================================
0x00    integer   Number of user defined controllers (0 to 27)
0x01    flag      Arpeggiator
0x02    flag      Apply velocity to project
0x03    inverted  Event output
======  ========  ============================================

MultiSynth options
..................

======  ========  ==========================================================
Offset  Type      Purpose
======  ========  ==========================================================
0x00    flag      Use static note C5
0x01    flag      Ignore notes with zero velocity
0x02    flag      0x00 = note/velocity curve, 0x01 = velocity/velocity curve
======  ========  ==========================================================

Sampler
.......

======  ========  ========================================
Offset  Type      Purpose
======  ========  ========================================
0x00    flag      Record on play
0x01    flag      Record in mono
0x02    flag      Record with reduced sample rate
0x03    flag      Record in 16-bit
0x04    flag      Stop recording on project stop
0x05    flag      Ignore velocity for volume
======  ========  ========================================

Sound2Ctl
.........

======  ========  ========================================
Offset  Type      Purpose
======  ========  ========================================
0x00    flag      Record values
======  ========  ========================================

Array chunk
-----------

Some module-specific chunks are in the form of an array.
Such an array will be described using these attributes:

- ``CHNM`` number
- Length (in values)
- Data type
- Minimum value
- Maximum value
- Default value

Analog Generator module-specific chunks
---------------------------------------

To be documented.

Generator module-specific chunks
--------------------------------

To be documented.

MetaModule module-specific chunks
---------------------------------

To be documented.

MultiCtl module-specific chunks
-------------------------------

To be documented.

MultiSynth module-specific chunks
---------------------------------

To be documented.

Sampler module-specific chunks
------------------------------

..  note::

    This is only accurate through SunVox 1.9.2.
    Efforts are underway to update this to reflect SunVox 1.9.3-beta1.

CHNM 0 - global sampler data
............................

The ``CHDT`` chunk for this section contains global sampler configuration
such as options, envelopes, and note mappings.

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    zeros             Reserved (offset 0x00 to 0x1b)
0x1c    unsigned int32    Max sample index + 1 (0 for no samples)
0x20    zeros             Reserved (offset 0x20 to 0x23)
0x24    unsigned int8     Sample number for note C-0 (note 0)
 ...     ...               ...
0x83    unsigned int8     Sample number for note B-8 (note 95)
0x84                      Volume envelope point 0
0x84    unsigned int16    - X Position (always 0 for point 0)
0x86    unsigned int16    - Y Position (0x00 to 0x40)
0x88                      Volume envelope point 1
0x8c                      Volume envelope point 2
0x90                      Volume envelope point 3
0x94                      Volume envelope point 4
0x98                      Volume envelope point 5
0x9c                      Volume envelope point 6
0xa0                      Volume envelope point 7
0xa4                      Volume envelope point 8
0xa8                      Volume envelope point 9
0xac                      Volume envelope point 10
0xb0                      Volume envelope point 11
0xb4                      Panning envelope point 0
0xb4    unsigned int16    - X Position (always 0 for point 0)
0xb6    unsigned int16    - Y Position (0x00 to 0x40, center at 0x20)
0xb8                      Panning envelope point 1
0xbc                      Panning envelope point 2
0xc0                      Panning envelope point 3
0xc4                      Panning envelope point 4
0xc8                      Panning envelope point 5
0xcc                      Panning envelope point 6
0xd0                      Panning envelope point 7
0xd4                      Panning envelope point 8
0xd8                      Panning envelope point 9
0xdc                      Panning envelope point 10
0xe0                      Panning envelope point 11
0xe4    unsigned int8     Number of active volume envelope points
0xe5    unsigned int8     Number of active panning envelope points
0xe6    unsigned int8     Volume sustain point
0xe7    unsigned int8     Volume loop start point
0xe8    unsigned int8     Volume loop end point
0xe9    unsigned int8     Pan sustain point
0xea    unsigned int8     Pan loop start point
0xeb    unsigned int8     Pan loop end point
0xec    bitmap            Volume `envelope bitmap`_
0xed    bitmask           Panning `envelope bitmap`_
0xee    unsigned int8     Vibrato type (0 = sin, 1 = saw, 2 = square)
0xef    unsigned int8     Vibrato attack
0xf0    unsigned int8     Vibrato depth
0xf1    unsigned int8     Vibrato rate (0x00 to 0x3f)
0xf2    unsigned int16    Volume fadeout (0x0000 to 0x2000)
0xf4    constant          Hex bytes 40 00 80 00 00 00 00 00
0xfc    constant          ASCII string 'PMAS'
0x100   constant          Hex bytes 04 00 00 00
0x104   unsigned int8     Sample number for note C-0 (note 0)
 ...     ...               ...
0x17a   unsigned int8     Sample number for note b-9 (note 118)
0x17b   zeros             Reserved (offset 0x17b to 0x183)
======  ================  ===================================================

Envelope bitmap
~~~~~~~~~~~~~~~

=====   ==============
Value   Purpose
=====   ==============
0x01    Enable
0x02    Sustain
0x04    Loop
=====   ==============

CHNM (n * 2 + 1)
................

(Where *n* is the sample index, starting at 0.)

The ``CHDT`` chunk for these sections contains sample-specific configuration
such as loop points, panning, and relative note information.

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    unsigned int32    Sample length, in frames
0x04    unsigned int32    Loop start frame
0x08    unsigned int32    Loop end frame
0x0c    unsigned int8     Volume (0 to 64)
0x0d    signed int8       Finetune (-128 to 127, center at 0)
0x0e    bitmap            `Loop and format bitmap`_
0x0f    unsigned int8     Panning (0 to 255, center at 128)
0x10    signed int8       Relative note (-128 to 127, center at 0)
0x11    zeros             Reserved (offset 0x11 to 0x27)
======  ================  ===================================================

Loop and format bitmap
~~~~~~~~~~~~~~~~~~~~~~

Bits 0-2 specify looping options:

=====   ==============
Value   Purpose
=====   ==============
0x00    No loop
0x01    Loop
0x02    Ping-pong loop
=====   ==============

Bits 3-5 specify sample format:

=====   =================
Value   Purpose
=====   =================
0x00    8-bit signed int
0x10    16-bit signed int
0x20    32-bit float
=====   =================

Bit 6 is a stereo flag:

=====   =================
Value   Purpose
=====   =================
0x00    mono
0x40    stereo
=====   =================

CHNM (n * 2 + 2)
................

(Where *n* is the sample index, starting at 0.)

The ``CHDT`` chunk for this section contains sample values
of the type specified by the ``CHFF`` chunk.

SpectraVoice module-specific chunks
-----------------------------------

To be documented.

Vorbis player module-specific chunks
------------------------------------

To be documented.

WaveShaper module-specific chunks
---------------------------------

WaveShaper curve chunk
......................

This is an `array chunk`_:

- ``CHNM`` number: 0x00
- Length (in values): 256
- Data type: unsigned int16
- Minimum value: 0x0000
- Maximum value: 0xffff
- Default value: Linear curve, x * 0x100
