from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module


class Sampler(Module):

    name = mtype = 'Sampler'
    mgroup = 'Synth'

    class SampleInterpolation(IntEnum):
        OFF = 0
        LINEAR = 1
        SPLINE = 2

    class EnvelopeInterpolation(IntEnum):
        OFF = 0
        LINEAR = 1

    # TODO: CHNK, CHNM, CHDT, CHFF, CHFR

    volume = Controller((0, 512), 256)
    panning = Controller((-128, 128), 0)
    sample_interpoluation = Controller(SampleInterpolation, SampleInterpolation.SPLINE)
    envelope_interpolation = Controller(EnvelopeInterpolation, EnvelopeInterpolation.LINEAR)
    polyphony_ch = Controller((1, 32), 8)
    rec_threshold = Controller((0, 10000), 4)


EnvelopeInterpolation = Sampler.EnvelopeInterpolation
SampleInterpolation = Sampler.SampleInterpolation


"""
"""


"""
CHNK: 00000102

CHNM: 00000000
CHDT: 00000000: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ------------------------------------------------ ?
      00000010: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ------------------------------------ ?
                                                     ----------- max sample index + 1
                                                                 (0 for no samples)
      00000020: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----------- ?
                            -- sample number for note C-0 (note 0)
      00000030: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000040: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000050: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000060: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000070: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000080: 00 00 00 00 00 00 40 00  08 00 00 00 80 00 00 00  ......@.........
                         -- sample number for note B-8 (note 95)
                            ----- vol envelope: point 1 x position (always 0)
                                  ----- vol envelope: point 1 y position (00-40)
                                         ----- vol point 2 x
                                               ----- vol point 2 y
                                                     ----- vol point 3 x
                                                           ----- vol point 3 y
      00000090: 00 01 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----- point 4 x
                      ----- vol point 4 y
                            ----- vol point 5 x
                                  ----- vol point 5 y
                                         ----- vol point 6 x
                                               ----- vol point 6 y
                                                     ----- vol point 7 x
                                                           ----- vol point 7 y
      000000A0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----- vol point 8 x
                      ----- vol point 8 y
                            ----- vol point 9 x
                                  ----- vol point 9 y
                                         ----- vol point 10 x
                                               ----- vol point 10 y
                                                     ----- vol point 11 x
                                                           ----- vol point 11 y
      000000B0: 00 00 00 00 00 00 20 00  40 00 10 00 80 00 30 00  ...... .@.....0.
                ----- vol point 12 x
                      ----- vol point 12 y
                            ----- panning envelope: point 1 x position (always 0)
                                  ----- panning envelope: point 1 y position (00-40, 20=center)
                                         ----- pan point 2 x
                                               ----- pan point 2 y
                                                     ----- pan point 3 x
                                                           ----- pan point 3 y
      000000C0: B4 00 20 00 00 00 00 00  00 00 00 00 00 00 00 00  .. .............
                ----- point 4 x
                      ----- pan point 4 y
                            ----- pan point 5 x
                                  ----- pan point 5 y
                                         ----- pan point 6 x
                                               ----- pan point 6 y
                                                     ----- pan point 7 x
                                                           ----- pan point 7 y
      000000D0: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----- pan point 8 x
                      ----- pan point 8 y
                            ----- pan point 9 x
                                  ----- pan point 9 y
                                         ----- pan point 10 x
                                               ----- pan point 10 y
                                                     ----- pan point 11 x
                                                           ----- pan point 11 y
      000000E0: 00 00 00 00 04 04 00 00  00 00 00 00 03 00 00 00  ................
                ----- pan point 12 x
                      ----- pan point 12 y
                            -- number of active vol envelope points
                               -- number of active pan envelope points
                                  -- vol sustain point
                                     -- vol loop start point
                                         -- vol loop end point
                                            -- pan sustain point
                                               -- pan loop start point
                                                  -- pan loop end point
                                                     -- volume envelope bitmask: 1 = enable, 2 = sustain, 4 = loop
                                                        -- panning envelope bitmask: 1 = enable, 2 = sustain, 4 = loop
                                                           -- vibrato type: 0=sin, 1=saw, 2=square
                                                              -- vibrato attack (0-255)
      000000F0: 00 00 00 00 40 00 80 00  00 00 00 00 50 4D 41 53  ....@.......PMAS
                -- vibrato depth (0-255)
                   -- vibrato rate (0-63)
                      ----- volume fadeout (0-8192)
                            ----- ?
                                  ----- ?
                                         ----------- ?
                                                     ----------- magic (little-endian SAMP)
      00000100: 04 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                ----------- ?
                            -- sample number for note C-0 (note 0)
      00000110: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000120: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000130: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000140: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000150: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000160: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
      00000170: 00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                                               -- sample number for note b-9 (note 118)
                                                  -- ?
                                                     ----------- ?
      00000180: 00 00 00 00                                       ....
                ----------- ?

CHNM: (sample number * 2 + 1)
CHDT: 00000000: C7 08 00 00 00 00 00 00  00 00 00 00 40 64 00 80  ............@d..
                ----------- length (frames)
                            ----------- loop start frame
                                         ----------- loop end frame
                                                     -- volume (0-64)
                                                        -- finetune (-128-127, 0x00-0xFF, signed, center=0x00)
                                                           -- 0x_0 = no loop
                                                           -- 0x_1 = loop
                                                           -- 0x_2 = ping-pong loop
                                                           -- 0x0_ = 8-bit mono
                                                           -- 0x1_ = 16-bit mono
                                                           -- 0x2_ = 32-bit mono
                                                           -- add 0x40 for stereo
                                                              -- panning (-128-127, 0x00-0xFF, unsigned w/ offset, center = 0x80)
      00000010: 10 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  ................
                -- relative note (-128-127, signed, center=0x00)
      00000020: 00 00 00 00 00 00 00 00                           ........
CHFF: 0
CHFR: 0

CHNM: (sample number * 2 + 2)
CHDT: <sample data, signed>
CHFF: format:
        1 - 8-bit mono
        2 - 16-bit mono
        4 - 32-bit mono
        9 - 8-bit stereo
        A - 16-bit stereo
        C - 32-bit stereo
CHFR: sample rate

CHNM: 00000101
CHDT: options (64 bytes)
        0: record on play
        1: record in mono
        2: record with reduced sample rate
        3: record in 16 bit
        4-63: zero padding
CHFF: 0
CHFR: 0
"""
