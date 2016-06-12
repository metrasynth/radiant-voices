from chunk import Chunk


def chunks(f):
    while True:
        try:
            c = Chunk(f, align=False, bigendian=False)
            yield c
            c.skip()
        except EOFError:
            break
