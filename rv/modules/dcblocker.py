from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


@register
class DcBlockerModule(Module):

    name = mtype = 'DC Blocker'

    channels = Controller(Channels, Channels.STEREO)
