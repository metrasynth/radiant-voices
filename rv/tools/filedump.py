import sys

import yaml

from rv.reader.readsunvoxfile import read_sunvox_file


if __name__ == '__main__':
    sf = read_sunvox_file(sys.argv[1])
    yaml.dump(sf, sys.stdout)
