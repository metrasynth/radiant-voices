"""A SunVox command line player with debugging tools.

Usage: python -m rv.tools.player FILE

Rather than load a SunVox project and play it directly,
this player will first load it into Python structures,
then save it back to an in-memory buffer,
then play that resulting project using SunVox DLL.
"""

import argparse
import logging
import sys
from os import unlink
from tempfile import mkstemp

from rv.api import ENCODING, Project, Synth, read_sunvox_file

log = logging.getLogger(__name__)


parser = argparse.ArgumentParser(description="Radiant Voices Player")
parser.add_argument(
    "filename", metavar="FILE", type=str, nargs=1, help="File to load and play"
)
parser.add_argument(
    "--bypass-rv",
    dest="skip_rv",
    action="store_const",
    const=True,
    default=False,
    help="Skip Radiant Voices and play directly using SunVox",
)
parser.add_argument(
    "--send-event",
    dest="send_event",
    action="store",
    metavar="TRACK,NOTE,VEL,MODULE,CTL,EFFECT,VAL",
    default=None,
    help="Instead of playing, send a command",
)


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        import sunvox.api
    except ImportError:
        log.error("Please install sunvox-dll-python to use rv.tools.player")
        log.error("https://github.com/metrasynth/sunvox-dll-python")
        return 1
    args = parser.parse_args()
    filename = args.filename[0]
    if args.skip_rv:
        log.debug("Skipping Radiant Voices")
        obj = filename
    else:
        log.debug("Loading into Radiant Voices")
        obj = read_sunvox_file(filename)
    sunvox.api.init(None, 44100, 2, 0)
    slot = sunvox.api.Slot()
    if isinstance(obj, Project):
        slot.load(obj)
    elif isinstance(obj, Synth):
        _, filename = mkstemp()
        filename = filename.encode("utf8")
        try:
            with open(filename, "wb") as f:
                obj.write_to(f)
            slot.load_module(filename, 0, 0, 0)
            slot.connect_module(1, 0)
            slot.volume(255)
        finally:
            unlink(filename)
    elif isinstance(obj, str):
        filename = obj.encode("utf8")
        if obj.endswith(".sunvox"):
            slot.load_filename(filename)
        elif obj.endswith(".sunsynth"):
            slot.load_module(filename, 0, 0, 0)
            slot.connect_module(1, 0)
            slot.volume(255)
        else:
            log.warning("Unknown file extension")
    module_count = slot.get_number_of_modules()
    log.info("{} modules loaded".format(module_count))
    for i in range(module_count):
        log.debug("module {}: {}".format(i, slot.get_module_name(i).decode(ENCODING)))
    if args.send_event is not None:
        event_args = [int(x) for x in args.send_event.split(",")]
        log.debug("event_args {!r}".format(event_args))
        track, note, vel, module, ctl, effect, val = event_args
        ctl_effect = ctl << 16 + effect
        slot.send_event(track, note, vel, module, ctl_effect, val)
    else:
        slot.play_from_beginning()
    print("Press Enter to stop playback")
    input()
    slot.stop()
    sunvox.api.deinit()


if __name__ == "__main__":
    sys.exit(main())
