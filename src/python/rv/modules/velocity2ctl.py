from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.velocity2ctl import BaseVelocity2Ctl


class Velocity2Ctl(BaseVelocity2Ctl, Module):

    flags = 0x020049

    behaviors = {B.receives_notes, B.sends_controls}
