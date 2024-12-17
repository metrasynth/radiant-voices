# -- DO NOT EDIT THIS FILE DIRECTLY --
"""
Base class for Sound2Ctl
This file was auto-generated by genrv.
"""
from enum import IntEnum

from rv.controller import Controller
from rv.option import Option


class BaseSound2Ctl:
    name = "Sound2Ctl"
    mtype = "Sound2Ctl"
    mgroup = "Misc"
    flags = default_flags = 0x60051

    class Channels(IntEnum):
        mono = 0
        stereo = 1

    class Mode(IntEnum):
        lq = 0
        hq = 1

    sample_rate = Controller((1, 32768), 50)
    channels = Controller(Channels, Channels.mono)
    absolute = Controller(bool, True)
    gain = Controller((0, 1024), 256)
    smooth = Controller((0, 256), 128)
    mode = Controller(Mode, Mode.hq)
    out_min = Controller((0, 32768), 0)
    out_max = Controller((0, 32768), 32768)
    out_controller = Controller((0, 255), 0)
    record_values = Option(
        name="record_values",
        number=127,
        byte=0,
        bit=0,
        size=1,
        default=False,
    )
    send_only_changed_values = Option(
        name="send_only_changed_values",
        number=126,
        byte=1,
        bit=0,
        size=1,
        default=True,
    )
