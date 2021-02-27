from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.echo import BaseEcho


class Echo(BaseEcho, Module):

    behaviors = {B.receives_audio, B.sends_audio}
