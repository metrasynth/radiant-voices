SunVox File Format
==================

This document is an ongoing effort to describe the SunVox file format
in a way that is useful to developers of Radiant Voices
(and other apps that want to read/write SunVox files).

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

Contains an entire SunVox project.

sunsynth
........

Contains a single SunVox module.

sunpat
......

Contains a single pattern.

sunpats
.......

Contains multiple patterns.

Sampler chunks
--------------

The Sampler module is by far the most complex of the SunVox module types,
so we dedicate an entire section to its data structures.

..  note::

    This is only accurate through SunVox 1.9.2.
    Efforts are underway to update this to reflect SunVox 1.9.3-beta1.

CHNM 0 - global sampler data
...........................

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
0xec    bitmask           Volume envelope bitmask (see below)
0xed    bitmask           Panning envelope bitmask (see below)
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

Envelope bitmasks
~~~~~~~~~~~~~~~~~

=====   ==============
Value   Purpose
=====   ==============
0x01    Enable
0x02    Sustain
0x04    Loop
=====   ==============

CHNM (n * 2 + 1)
...............

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
0x0e    bitmap (1 byte)   Loop and format bitmap (see below)
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
...............

(Where *n* is the sample index, starting at 0.)

The ``CHDT`` chunk for this section contains sample values
of the type specified by the ``CHFF`` chunk.

The ``CHFF`` chunk is an unsigned int32.
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

The ``CHFR`` chunk is an unsigned int32,
specifying the sample rate.
