from rv.structure.controller import Controller, Choices, Range
from rv.structure.module import GenericModule


class InputModule(GenericModule):

    class controllers(object):

        volume = Controller(
            0x01, 'Volume', 0, 1024, Range(0, 1024))

        channels = Controller(
            0x02, 'Channels', 0, 1, Choices('mono', 'stereo'))
