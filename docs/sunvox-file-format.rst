SunVox File Format
==================

This document describes the SunVox file format
in a way that is useful to developers of any app
that wants to read/write SunVox files.

Special thanks to Alexander Zolotov for helping complete this document,
and for sharing SunVox and his other creative works with the world.

This document reflects SunVox 1.9.4.

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

    You can use Radiant Voices to quickly inspect the IFF structure
    of a SunVox file::

        $ python -m rv.lib.iff myproject.sunvox

        SVOX

        VERS  00000000: 00 03 09 01                                       ....

        BVER  00000000: 00 02 09 01                                       ....

        BPM   00000000: 7D 00 00 00                                       }...

        [ ... ]

String encoding
---------------

All strings are UTF-8 encoded C-style strings.

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

2.  SunVox version: ``VERS`` type, unsigned int32.
    (e.g. 0x01090300 for v1.9.3.0)

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
``VERS``  unsigned int32    SunVox version (e.g. 0x01090300 for v1.9.3.0)
``BVER``  unsigned int32    Based-on version
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
``REPS``  signed int32      Restart position
``SELS``  unsigned int32    Index of Last selected module
``LGEN``  unsigned int32    Index of last selected generator module
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

========  ==========================
Value     Purpose
========  ==========================
0x01      No icon
========  ==========================

Pattern flags
.............

========  ==========================
Value     Purpose
========  ==========================
0x01      Clone of another pattern
0x02      Pattern is selected
0x08      Mute
0x10      Solo
========  ==========================

Module chunks
-------------

If a module doesn't exist at a given index,
the only chunk present will be ``SEND``.

========  ====================  =================================================================
Type ID   Format                Purpose
========  ====================  =================================================================
``SFFF``  bitmap (4 bytes)      `Module flags`_
``SNAM``  string[32]            Module name (zero-padded)
``STYP``  cstring               Module type (not present for "Output" module)
``SFIN``  signed int32          Finetune
``SREL``  signed int32          Relative note
``SXXX``  signed int32          X position (not in sunsynth files)
``SYYY``  signed int32          Y position (not in sunsynth files)
``SZZZ``  signed int32          Layer (not in sunsynth files)
``SSCL``  unsigned int32        Scale
``SVPR``  bitmap (4 bytes)      `Module visualization bitmap`_ (not in sunsynth files)
``SCOL``  bytes[3]              Color (RGB)
``SMII``  unsigned int32        `MIDI in`_
``SMIN``  cstring               MIDI Out name (not present if none selected)
``SMIC``  unsigned int32        MIDI Out channel (0 for all channels)
``SMIB``  signed int32          MIDI Out bank (-1 for none)
``SMIP``  signed int32          MIDI Out program (-1 for none)
``SLNK``  signed int32[n]       Module indexes of incoming links, optionally terminated with -1
``CVAL``  unsigned int32        Controller value for controller 1
 ...       ...                   ...
``CVAL``  unsigned int32        Controller value for controller *n*
``CMID``  bytes[8]              `Controller MIDI mappings`_ for controller 1
 ...       ...                   ...
``CMID``  bytes[8]              `Controller MIDI mappings`_ for controller *n*
``CHNK``  unsigned int32        `CHNK value`_ for the module, if applicable
multiple                        `Module-specific chunks`_, if applicable
========  ====================  =================================================================

Module flags
............

User-accessible module flags:

======  ==========================
Value   Purpose
======  ==========================
0x80    Mute
0x100   Solo
0x4000  Bypass
======  ==========================

Internal module flags:

========  ==========================
Value     Purpose
========  ==========================
0x000001  Exists
0x000002  Output
0x000008  Generator
0x000010  Effect
0x000040  Initialized
0x000400  Get speed changes
0x000800  Hidden
0x001000  Multi
0x002000  Don't fill input
0x008000  Use mutex
0x010000  Ignore mute
0x020000  No scope buffer
0x040000  Output is empty
0x080000  Open
0x100000  Get play commands
0x200000  Get render setup commands
0x400000  Feedback
0x800000  Get stop commands
========  ==========================

Default flags for each module type:

====================  ========
Module type           Default
====================  ========
Amplifier             0x000051
Analog generator      0x000049
Compressor            0x002051
DC Blocker            0x000051
Delay                 0x000451
Distortion            0x000051
DrumSynth             0x000049
Echo                  0x000451
EQ                    0x000051
Feedback              0x600051
Filter                0x000451
Filter Pro            0x000451
Flanger               0x000451
FM                    0x000049
Generator             0x000059
Glide                 0x021049
GPIO                  0x000051
Input                 0x000049
Kicker                0x000049
LFO                   0x000451
Loop                  0x000451
MetaModule            0x008051
Modulator             0x002051
MultiCtl              0x020051
MultiSynth            0x021049
Output                0x000043
Pitch shifter         0x000051
Pitch2Ctl             0x020049
Reverb                0x000051
Sampler               0x008459
Sound2Ctl             0x600051
SpectraVoice          0x000049
Velocity2Ctl          0x020049
Vibrato               0x000451
Vocal filter          0x000051
Vorbis player         0x008049
WaveShaper            0x000051
====================  ========

Module visualization bitmap
...........................

======  ============================================
Bits    Purpose
======  ============================================
0-4     `Level mode`_
5-7     `Level flags`_
8-12    `Oscilloscope mode`_
13-15   Reserved for oscilloscope flags
16-23   Oscilloscope size in ms (unsigned int8)
24-25   BG transparency (0 = visible, 3 = invisible)
26-27   Shadow opacity (0 = invisible, 3 = visible)
28-31   Reserved for other flags
======  ============================================

Level mode
~~~~~~~~~~

======  ==========================
Value   Purpose
======  ==========================
0x00    Off
0x01    Mono
0x02    Stereo
0x03    Color
0x04    Glow
======  ==========================

Level flags
~~~~~~~~~~~

=====   ==========================================
Value   Purpose
=====   ==========================================
0x01    Orientation (0 = horizontal, 1 = vertical)
=====   ==========================================


Oscilloscope mode
~~~~~~~~~~~~~~~~~

======  ==========================
Value   Purpose
======  ==========================
0x00    Off
0x01    Points
0x02    Lines
0x03    Bars
0x04    Bars 2 (symmetrical)
0x05    Stereo Phase Scope × 1
0x06    Stereo Phase Scope × 2
0x07    XY
======  ==========================

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

This must be at least 1 more than the maximum ``CHNM`` used by the module.

It is used to allocate space in SunVox,
and the audio engine will stop if the ``CHNM`` is too small.

Module-specific chunks
----------------------

General format
..............

========  ====================  =======================================================
Type ID   Format                Purpose
========  ====================  =======================================================
``CHNM``  unsigned int32        Module-specific chunk number
``CHDT``  (module-dependent)    Module-specific chunk data
========  ====================  =======================================================

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
0x03    flag      Trigger (ignore note off)
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

Array values are stored in the ``CHDT`` in row order.

Waveform chunk
--------------

These types of chunks contain sample data in their ``CHDT``,
and have two additional IFF chunks:

========  ====================  =========================================================
Type ID   Format                Purpose
========  ====================  =========================================================
``CHFF``  bitmap (4 bytes)      `Chunk audio format bitmap`_
``CHFR``  unsigned int32        Chunk audio freq (default 44100; not written if default)
========  ====================  =========================================================

Chunk audio format bitmap
.........................

The first 3 bits specify the format, and the 4th bit is a stereo flag:

=====   =================   ======
Value   Format              Stereo
=====   =================   ======
0x00    ?                   ?
0x01    8-bit signed int    No
0x02    16-bit signed int   No
0x04    32-bit float        No
0x09    8-bit signed int    Yes
0x0a    16-bit signed int   Yes
0x0c    32-bit float        Yes
=====   =================   ======

Drawn waveform chunk
....................

This is a waveform chunk that has some restrictions:

- Fixed length of 32 frames
- Fixed format of mono, 8-bit
- Fixed freq of 44100

SunVox assigns a default waveform::

    00 9C A6 00 5A 89 EC 2D 02 EC 6F E9 02 9E 3C 20
    64 32 00 CE 41 62 32 20 A6 88 64 5A 3B 15 00 36


Analog Generator module-specific chunks
---------------------------------------

Analog Generator drawn waveform (CHNM 0)
........................................

This is a `drawn waveform chunk`_.

Generator module-specific chunks
--------------------------------

Generator drawn waveform (CHNM 0)
.................................

This is a `drawn waveform chunk`_.

MetaModule module-specific chunks
---------------------------------

MetaModule embedded project (CHNM 0)
....................................

The ``CHDT`` contains the binary data for the embedded SunVox project,
in the same format as a sunvox_ file.

MetaModule user defined controller mappings (CHNM 1)
....................................................

This is an `array chunk`_:

- Length (in values): 64
- Data type: 4-byte structure (see below)

Each item in the array describes a mapping between a user-defined controller
and a target module/controller in the embedded project.

Only the first 27 items are used, as that is the maximum number of
user defined controllers. The remaining items are always unset.

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    unsigned int16    Target module index (0x00 for unset)
0x02    unsigned int16    Target controller number (1-based, 0x00 for unset)
======  ================  ===================================================

MetaModule user defined controller names (CHNM 8+n)
...................................................

Where *n* is the 0-based index of the user-defined controller.

The ``CHDT`` contains a cstring with the controller name.

MultiCtl module-specific chunks
-------------------------------

MultiCtl mapping array (CHNM 0)
...............................

This is an `array chunk`_:

- Length (in values): 16
- Data type: 32-byte structure (see below)

Each item in the array corresponds to a downstream module.
Items are ordered by module index.
Items past the number of connected downstream modules are ignored.

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    unsigned int32    Minimum value
0x02    unsigned int32    Maximum value
0x04    unsigned int32    Controller number (1-based index)
0x06    unsigned int32    Reserved (0x00 value)
0x08    unsigned int32    Reserved (0x00 value)
0x0a    unsigned int32    Reserved (0x00 value)
0x0c    unsigned int32    Reserved (0x00 value)
0x0e    unsigned int32    Reserved (0x00 value)
======  ================  ===================================================

MultiCtl value curve (CHNM 1)
.............................

This is an `array chunk`_:

- Length (in values): 257
- Data type: unsigned int16
- Minimum value: 0x0000
- Maximum value: 0x8000
- Default value: Linear curve, ``x * 0x80``

MultiSynth module-specific chunks
---------------------------------

MultiSynth note/velocity curve (CHNM 0)
.......................................

This is an `array chunk`_:

- Length (in values): 128
- Data type: unsigned int8
- Minimum value: 0x00
- Maximum value: 0xff
- Default value: 0xff

MultiSynth velocity/velocity curve (CHNM 2)
...........................................

This is an `array chunk`_:

- Length (in values): 257
- Data type: unsigned int8
- Minimum value: 0x00
- Maximum value: 0xff
- Default value: Linear curve, ``min(x, 255)``

Sampler module-specific chunks
------------------------------

Sampler global configuration (CHNM 0)
.....................................

The ``CHDT`` chunk for this section contains global sampler configuration
such as options, envelopes, and note mappings.

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    zeros             Reserved (offset 0x00 to 0x1b)
0x1c    unsigned int32    Max sample index + 1 (0 for no samples)
0x20    zeros             Reserved (offset 0x20 to 0x23)
0x24    unsigned int8     Legacy sample number for note C-0 (note 0)
 ...     ...               ...
0x83    unsigned int8     Legacy sample number for note B-8 (note 95)
0x84                      Legacy volume envelope point 0
0x84    unsigned int16    - X Position (always 0 for point 0)
0x86    unsigned int16    - Y Position (0x00 to 0x40)
0x88                      Legacy volume envelope point 1
0x8c                      Legacy volume envelope point 2
0x90                      Legacy volume envelope point 3
0x94                      Legacy volume envelope point 4
0x98                      Legacy volume envelope point 5
0x9c                      Legacy volume envelope point 6
0xa0                      Legacy volume envelope point 7
0xa4                      Legacy volume envelope point 8
0xa8                      Legacy volume envelope point 9
0xac                      Legacy volume envelope point 10
0xb0                      Legacy volume envelope point 11
0xb4                      Legacy panning envelope point 0
0xb4    unsigned int16    - X Position (always 0 for point 0)
0xb6    unsigned int16    - Y Position (0x00 to 0x40, center at 0x20)
0xb8                      Legacy panning envelope point 1
0xbc                      Legacy panning envelope point 2
0xc0                      Legacy panning envelope point 3
0xc4                      Legacy panning envelope point 4
0xc8                      Legacy panning envelope point 5
0xcc                      Legacy panning envelope point 6
0xd0                      Legacy panning envelope point 7
0xd4                      Legacy panning envelope point 8
0xd8                      Legacy panning envelope point 9
0xdc                      Legacy panning envelope point 10
0xe0                      Legacy panning envelope point 11
0xe4    unsigned int8     Legacy number of active volume envelope points
0xe5    unsigned int8     Legacy number of active panning envelope points
0xe6    unsigned int8     Legacy volume sustain point
0xe7    unsigned int8     Legacy volume loop start point
0xe8    unsigned int8     Legacy volume loop end point
0xe9    unsigned int8     Legacy pan sustain point
0xea    unsigned int8     Legacy pan loop start point
0xeb    unsigned int8     Legacy pan loop end point
0xec    bitmap            Legacy volume `envelope bitmap`_
0xed    bitmask           Legacy panning `envelope bitmap`_
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

Sample configuration chunk (CHNM n*2+1)
.......................................

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

Sample waveform (CHNM n*2+2)
............................

(Where *n* is the sample index, starting at 0.)

This is a `waveform chunk`_.

Sample envelope chunk
.....................

======  ================  ===================================================
Offset  Type              Purpose
======  ================  ===================================================
0x00    unsigned int16    `Sample envelope flags`_
0x02    unsigned int8     Controller number (0x00 to 0x1f)
0x03    unsigned int8     Gain percentage (0x00 to 0x64)
0x04    unsigned int8     Velocity (0x00 to 0x64)
0x05    unknown           00 00 00
0x08    unsigned int16    Number of points in envelope
0x0a    unsigned int16    Sustain point
0x0c    unsigned int16    Loop start point
0x0e    unsigned int16    Loop end point
0x10    unknown           00 00 00 00
0x14    unsigned int16    X position of point 1 (in ticks)
0x16    unsigned int16    Y position of point 1 (0x0000 to 0x8000)
 ...     ...               ...
 ...    unsigned int16    X position of point *n*
 ...    unsigned int16    Y position of point *n*
======  ================  ===================================================

Sample envelope flags
.....................

=====   =================
Value   Purpose
=====   =================
0x01    enabled
0x02    sustain
0x04    loop
=====   =================

Volume envelope (CHNM 0x102)
............................

This is a `sample envelope chunk`_.

Panning envelope (CHNM 0x103)
.............................

This is a `sample envelope chunk`_.

Pitch envelope (CHNM 0x104)
...........................

This is a `sample envelope chunk`_.

Effect control 1 envelope (CHNM 0x105)
......................................

This is a `sample envelope chunk`_.

Effect control 2 envelope (CHNM 0x106)
......................................

This is a `sample envelope chunk`_.

Effect control 3 envelope (CHNM 0x107)
......................................

This is a `sample envelope chunk`_.

Effect control 4 envelope (CHNM 0x108)
......................................

This is a `sample envelope chunk`_.

Sampler effect module (CHNM 0x10a)
..................................

This contains the selected effect, serialized as a sunsynth_.

SpectraVoice module-specific chunks
-----------------------------------

SpectraVoice harmonic frequencies (CHNM 0)
..........................................

This is an `array chunk`_:

- Length (in values): 16
- Data type: unsigned int16
- Minimum value: 0x0000
- Maximum value: 0x8000
- Default value: [0x044a, 0x00, ...]

SpectraVoice harmonic volumes (CHNM 1)
......................................

This is an `array chunk`_:

- Length (in values): 16
- Data type: unsigned int8
- Minimum value: 0x00
- Maximum value: 0xff
- Default value: [0xff, 0x00, ...]

SpectraVoice harmonic widths (CHNM 2)
.....................................

This is an `array chunk`_:

- Length (in values): 16
- Data type: unsigned int8
- Minimum value: 0x00
- Maximum value: 0xff
- Default value: [0x03, 0x00, ...]

SpectraVoice harmonic types (CHNM 3)
....................................

This is an `array chunk`_:

- Length (in values): 16
- Data type: byte enumeration (see below)
- Default value: [hsin, ...]

======  ======================
Value   Purpose
======  ======================
0x00    hsin
0x01    rect
0x02    org1
0x03    org2
0x04    org3
0x05    org4
0x06    sin
0x07    random
0x08    triangle1
0x09    triangle2
0x0a    overtones1
0x0b    overtones2
0x0c    overtones3
0x0d    overtones4
======  ======================

Vorbis player module-specific chunks
------------------------------------

Vorbis player file data chunk (CHNM 0)
......................................

``CHDT`` contains the Vorbis file content,
or is empty if no file has been loaded.

WaveShaper module-specific chunks
---------------------------------

WaveShaper curve chunk (CHNM 0)
...............................

This is an `array chunk`_:

- Length (in values): 256
- Data type: unsigned int16
- Minimum value: 0x0000
- Maximum value: 0xffff
- Default value: Linear curve, ``x * 0x100``
