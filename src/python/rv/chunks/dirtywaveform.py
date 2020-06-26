from .waveform import WaveformChunk


class DirtyWaveformChunk(WaveformChunk):

    fixed_length = 32
    fixed_format = WaveformChunk.Format.mono_8bit
    fixed_freq = 44100

    default = (
        b"\x00"
        b"\x9C"
        b"\xA6"
        b"\x00"
        b"\x5A"
        b"\x89"
        b"\xEC"
        b"\x2D"
        b"\x02"
        b"\xEC"
        b"\x6F"
        b"\xE9"
        b"\x02"
        b"\x9E"
        b"\x3C"
        b"\x20"
        b"\x64"
        b"\x32"
        b"\x00"
        b"\xCE"
        b"\x41"
        b"\x62"
        b"\x32"
        b"\x20"
        b"\xA6"
        b"\x88"
        b"\x64"
        b"\x5A"
        b"\x3B"
        b"\x15"
        b"\x00"
        b"\x36"
    )


__all__ = ["DirtyWaveformChunk"]
