from rv.controller import Controller
from rv.modules import Behavior as B, Module
from rv.modules.base.feedback import BaseFeedback


class Feedback(BaseFeedback, Module):

    flags = 0x600051

    behaviors = {B.receives_audio, B.receives_feedback, B.sends_audio, B.sends_feedback}

    Channels = BaseFeedback.Channels

    volume = Controller((0, 10000), 1000)
    channels = Controller(Channels, Channels.stereo)
