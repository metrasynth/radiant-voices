from __future__ import annotations

import logging
from pathlib import Path
from typing import TYPE_CHECKING, Union

from logutils import BraceMessage as _F
from rv import ENCODING
from rv.lib.iff import chunks

if TYPE_CHECKING:
    from rv.project import Project
    from rv.synth import Synth

log = logging.getLogger(__name__)


def read_sunvox_file(file_or_name) -> Union[Project, Synth]:
    from rv.readers.initial import InitialReader

    close = False
    if isinstance(file_or_name, (Path, str)):
        file_or_name = Path(file_or_name).open("rb")
        close = True
    try:
        reader = InitialReader(file_or_name)
        return reader.object
    finally:
        if close:
            file_or_name.close()


class Reader:
    """Abstract base class for reading SunVox and SunSynth IFF files"""

    def __init__(self, f):
        self.f = f
        self._object = None

    @property
    def object(self):
        if self._object is None:
            self.process_chunks()
        return self._object

    @object.setter
    def object(self, value):
        if self._object is None:
            self._object = value
        else:
            raise AttributeError("object was already set")

    def process_chunks(self):
        try:
            for name, data in chunks(self.f):
                name = name.decode(ENCODING).strip()
                method_name = "process_{}".format(name)
                method = getattr(self, method_name, None)
                log_args = (self.__class__.__name__, method_name)
                if callable(method):
                    log.debug(_F("-> {}.{}", *log_args))
                    method(data)
                else:
                    log.warning(_F("no {}.{} method", *log_args))
            self.process_end_of_file()
        except ReaderFinished:
            pass

    def rewind(self, data):
        new_pos = self.f.tell() - len(data) - 8
        self.f.seek(new_pos)

    def process_PAMD(self, data):
        pass  # Unused in current SunVox.

    def process_end_of_file(self):
        raise RuntimeError("Reached end of file without a handler")


class ReaderFinished(Exception):
    """A reader is finished processing its relevant chunks."""
