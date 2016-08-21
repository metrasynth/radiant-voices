from enum import IntEnum

from rv.controller import Controller
from rv.modules import Module
from rv.modules import register


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


@register
class FeedbackModule(Module):

    type = name = 'Feedback'

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.STEREO)
