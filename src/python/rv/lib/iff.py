import struct

from rv._vendor.chunk import Chunk


def write_chunk(f, name, data):
    """Write the given name and data to file f (no-op if name is None)"""
    if name is None:
        return
    name = name[:4]
    name = name + b" " * (4 - len(name))
    size = len(data)
    f.write(name)
    f.write(struct.pack("<I", size))
    f.write(data)


def chunks(f):
    """Yield (name, data) chunks read from file f."""
    while True:
        try:
            c = Chunk(f, align=False, bigendian=False)
            yield c.getname(), c.read()
            c.skip()
        except EOFError:
            break


def dump_file(f, outfile=None):
    from hexdump import hexdump
    from rv import ENCODING

    for name, data in chunks(f):
        print(name.decode(ENCODING), end="  ", file=outfile)
        i = None
        for i, line in enumerate(hexdump(data, "generator")):
            if i > 0:
                print(f"      {line}", file=outfile)
            else:
                print(line, file=outfile)
        if i is None:
            print(file=outfile)
        print(file=outfile)


def dump_tool():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", metavar="FILE", type=str, nargs=1, help="File to load and dump"
    )
    args = parser.parse_args()
    filename = args.filename[0]
    with open(filename, "rb") as f:
        dump_file(f)


if __name__ == "__main__":
    dump_tool()
