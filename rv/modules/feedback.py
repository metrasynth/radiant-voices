from enum import IntEnum

from rv.controller import Controller
from rv.module import Module


class Channels(IntEnum):

    STEREO = 0
    MONO = 1


class FeedbackModule(Module):

    type = name = 'Feedback'

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.STEREO)
