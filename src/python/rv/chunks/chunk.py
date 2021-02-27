from struct import pack


class Chunk:

    chnm = None
    has_chff = False
    has_chfr = False

    def chunks(self):
        yield b"CHNM", pack("<I", self.chnm)
        yield b"CHDT", self.chdt()
        if self.has_chff:
            yield b"CHFF", self.chff()
        if self.has_chfr:
            yield b"CHFR", self.chfr()

    def chdt(self):
        return b""

    def chff(self):
        return pack("<I", 0)

    def chfr(self):
        return pack("<I", 0)
