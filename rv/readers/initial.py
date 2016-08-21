from rv.readers.reader import Reader, ReaderFinished
from rv.readers.sunvox import SunVoxReader


class InitialReader(Reader):

    def process_svox(self, _):
        self.object = SunVoxReader(self.f).object
        print('got {!r}'.format(self.object))

    def process_end_of_file(self):
        raise ReaderFinished()
