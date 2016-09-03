from rv.modules import Module


class Output(Module):
    """
    This is a special module that you should never create on your own.
    It is automatically created as module ``00`` of a :py:class:`Project`.
    """

    name = mtype = 'Output'
    mgroup = 'System'
    flags = 0x00000043
