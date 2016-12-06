from enum import Enum

from rv.controller import Controller
from rv.modules import Behavior as B, Module


class Feedback(Module):

    name = mtype = 'Feedback'
    mgroup = 'Misc'

    behaviors = {B.receives_audio, B.receives_feedback,
                 B.sends_audio, B.sends_feedback}

    class Channels(Enum):
        stereo = 0
        mono = 1

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.stereo)
