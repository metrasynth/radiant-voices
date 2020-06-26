from io import BytesIO

from rv.lib.iff import write_chunk
from rv.readers.reader import read_sunvox_file


class Container:
    def chunks(self):
        raise NotImplementedError()

    def read(self):
        with BytesIO() as f:
            self.write_to(f)
            return f.getvalue()

    def write_to(self, file):
        for chunk in self.chunks():
            write_chunk(file, *chunk)

    def clone(self):
        with BytesIO() as f:
            self.write_to(f)
            f.seek(0)
            return read_sunvox_file(f)
