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

CHNM (n * 2 + 1)
...............

(Where *n* is the sample number, starting at 0.)

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

(Where *n* is the sample number, starting at 0.)

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
