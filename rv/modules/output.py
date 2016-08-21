from rv.modules import Module
from rv.modules import register


@register
class OutputModule(Module):

    name = mtype = 'Output'
    flags = 0x00000043
