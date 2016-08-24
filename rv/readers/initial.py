from rv.readers.reader import Reader, ReaderFinished
from rv.readers.sunvox import SunVoxReader
from rv.readers.sunsynth import SunSynthReader


class InitialReader(Reader):

    def process_svox(self, _):
        self.object = SunVoxReader(self.f).object

    def process_ssyn(self, _):
        self.object = SunSynthReader(self.f).object

    def process_end_of_file(self):
        raise ReaderFinished()
