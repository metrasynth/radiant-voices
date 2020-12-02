from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.distortion import BaseDistortion


class Distortion(BaseDistortion, Module):

    behaviors = {B.receives_audio, B.sends_audio}
