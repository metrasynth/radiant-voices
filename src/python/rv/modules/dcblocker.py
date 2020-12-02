from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.dcblocker import BaseDcBlocker


class DcBlocker(BaseDcBlocker, Module):

    behaviors = {B.receives_audio, B.sends_audio}
