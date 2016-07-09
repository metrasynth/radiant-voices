from rv.structure.controller import Controller
from rv.structure.module import GenericModule
from .enums import Channels


class DcBlockerModule(GenericModule):

    class controller_types:
        channels = Controller(0x01, Channels)
