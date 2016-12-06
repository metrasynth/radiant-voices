from rv.modules import Behavior as B, Module


class Output(Module):
    """
    This is a special module that you should never create on your own.
    It is automatically created as module ``00`` of a :py:class:`Project`.
    """

    behaviors = {B.receives_audio}

    name = mtype = 'Output'
    mgroup = 'Output'
    flags = 0x00000043
    index = 0
