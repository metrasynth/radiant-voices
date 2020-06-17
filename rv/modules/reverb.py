from rv.controller import Controller
from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.reverb import BaseReverb


class Reverb(BaseReverb, Module):

    flags = 0x000051

    behaviors = {B.receives_audio, B.sends_audio}

    Mode = BaseReverb.Mode

    dry = Controller((0, 256), 256)
    wet = Controller((0, 256), 64)
    feedback = Controller((0, 256), 256)
    damp = Controller((0, 256), 128)
    stereo_width = Controller((0, 256), 256)
    freeze = Controller(bool, False)
    mode = Controller(Mode, Mode.hq)
    all_pass_filter = Controller(bool, True)
    room_size = Controller((0, 128), 16)
    random_seed = Controller((0, 32768), 0)
