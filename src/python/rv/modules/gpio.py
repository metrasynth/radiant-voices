from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.gpio import BaseGpio


class Gpio(BaseGpio, Module):

    behaviors = {B.receives_audio, B.sends_audio}
