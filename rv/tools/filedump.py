import sys

from rv.reader.readsunvoxfile import read_sunvox_file


if __name__ == '__main__':
    read_sunvox_file(sys.argv[1])
