import struct


def write_chunk(f, header, data):
    """Write the given header and data to file f (unless header is None)"""
    if header is None:
        return
    header = header[:4]
    header = header + b' ' * (4 - len(header))
    size = len(data)
    f.write(header)
    f.write(struct.pack('<I', size))
    f.write(data)
