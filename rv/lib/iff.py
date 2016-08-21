from chunk import Chunk
import struct


def write_chunk(f, name, data):
    """Write the given name and data to file f (no-op if name is None)"""
    if name is None:
        return
    name = name[:4]
    name = name + b' ' * (4 - len(name))
    size = len(data)
    f.write(name)
    f.write(struct.pack('<I', size))
    f.write(data)


def chunks(f):
    """Yield (name, data) chunks read from file f."""
    while True:
        try:
            c = Chunk(f, align=False, bigendian=False)
            yield (c.getname(), c.read())
            c.skip()
        except EOFError:
            break
