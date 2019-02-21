from rv.lib.iff import write_chunk       

def write_sunvox_bytes(project):
    from io import BytesIO
    buf=BytesIO()
    for name, value in project.chunks():
        if not name:
            continue
        write_chunk(buf, name, value)
    return buf.getvalue()

def write_sunvox_file(project, filename):
    with open(filename, 'wb') as f:
        for name, value in project.chunks():
            if not name:
                continue
            write_chunk(f, name, value)

if __name__=="__main__":
    import os
    try:
        os.mkdir("tmp")
    except:
        pass
    from rv.readers.reader import read_sunvox_file
    proj=read_sunvox_file("tracks/nightradio/city_dreams.sunvox")
    write_sunvox_file(proj, "tmp/city_dreams.sunvox")


