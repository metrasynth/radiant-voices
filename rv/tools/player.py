"""A SunVox command line player with debugging tools.

Usage: python -m rv.tools.player FILE

Rather than load a SunVox project and play it directly,
this player will first load it into Python structures,
then save it back to an in-memory buffer,
then play that resulting project using SunVox DLL.
"""

import argparse
import logging
log = logging.getLogger(__name__)

import sunvox

from rv import read_sunvox_file


parser = argparse.ArgumentParser(description='Radiant Voices Player')
parser.add_argument('filename', metavar='FILE', type=str, nargs=1,
                    help='File to load and play')
parser.add_argument('--skip-rv', dest='skip_rv', action='store_const',
                    const=True, default=False,
                    help='Skip Radiant Voices and play directly using SunVox')


def main():
    logging.basicConfig(level=logging.DEBUG)
    args = parser.parse_args()
    filename = args.filename[0]
    if args.skip_rv:
        log.debug('Skipping Radiant Voices')
        project = filename
    else:
        log.debug('Loading into Radiant Voices')
        project = read_sunvox_file(filename)
    sunvox.init(None, 44100, 2, 0)
    with sunvox.Slot(project) as slot:
        log.info('{} modules loaded'.format(slot.get_number_of_modules()))
        slot.play_from_beginning()
        print('Press Enter to stop playback')
        input()
        slot.stop()
    sunvox.deinit()


if __name__ == '__main__':
    main()
