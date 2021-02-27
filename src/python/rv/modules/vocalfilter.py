from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.vocalfilter import BaseVocalFilter


class VocalFilter(BaseVocalFilter, Module):

    behaviors = {B.receives_audio, B.sends_audio}
