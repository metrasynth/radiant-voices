from struct import pack


class Chunk(object):

    def chunks(self):
        yield (b'CHNM', pack('<I', self.chnm))
        yield (b'CHDT', self.chdt())
        yield (b'CHFF', self.chff())
        yield (b'CHFR', self.chfr())

    def chdt(self):
        return b''

    def chff(self):
        return pack('<I', 0)

    def chfr(self):
        return pack('<I', 0)
