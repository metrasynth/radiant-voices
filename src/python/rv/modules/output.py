from rv.modules import Behavior as B
from rv.modules import Module
from rv.modules.base.output import BaseOutput


class Output(BaseOutput, Module):
    """
    This is a special module that you should never create on your own.
    It is automatically created as module ``00`` of a :py:class:`Project`.
    """

    behaviors = {B.receives_audio}

    index = 0
