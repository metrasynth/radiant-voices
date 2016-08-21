import logging
from logutils import BraceMessage as _F
log = logging.getLogger(__name__)


from rv.modules.module import Module


class UnsupportedModule(Module):

    _mtype = 'Unsupported'

    @property
    def mtype(self):
        return self._mtype

    @mtype.setter
    def mtype(self, value):
        log.warn(_F('Unsupported module type {}', value))
        self._mtype = value
