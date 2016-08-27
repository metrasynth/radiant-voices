from io import BytesIO

from rv.lib.iff import write_chunk


class Container(object):

    def chunks(self):
        raise NotImplementedError()

    def read(self):
        with BytesIO() as file:
            self.write_to(file)
            return file.getvalue()

    def write_to(self, file):
        for chunk in self.chunks():
            write_chunk(file, *chunk)
