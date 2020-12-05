from .waveform import WaveformChunk


class DrawnWaveformChunk(WaveformChunk):

    fixed_length = 32
    fixed_format = WaveformChunk.Format.mono_8bit
    fixed_freq = 44100

    has_chfr = True

    default = [
        0,
        -100,
        -90,
        0,
        90,
        -119,
        -20,
        45,
        2,
        -20,
        111,
        -23,
        2,
        -98,
        60,
        32,
        100,
        50,
        0,
        -50,
        65,
        98,
        50,
        32,
        -90,
        -120,
        100,
        90,
        59,
        21,
        0,
        54,
    ]


__all__ = ["DrawnWaveformChunk"]
