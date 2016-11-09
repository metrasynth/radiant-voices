from struct import unpack

from rv.readers.module import ModuleReader
from rv.readers.reader import Reader, ReaderFinished
from rv.synth import Synth


class SunSynthReader(Reader):

    def __init__(self, f):
        super(SunSynthReader, self).__init__(f)

    def process_chunks(self):
        self.object = Synth()
        super().process_chunks()

    def process_vers(self, data):
        self.object.sunsynth_version, = unpack('<I', data)

    def process_sfff(self, data):
        self.rewind(data)
        module = ModuleReader(self.f, index=1).object
        self.object.module = module

    def process_end_of_file(self):
        raise ReaderFinished()
