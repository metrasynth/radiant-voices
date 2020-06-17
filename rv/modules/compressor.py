from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.compressor import BaseCompressor


class Compressor(BaseCompressor, Module):

    flags = 0x002051

    behaviors = {B.receives_audio, B.sends_audio}
