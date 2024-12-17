"""Render difference between rv-processed and native SunVox playback.

Used to validate that the SunVox IFF structure is preserved enough by Radiant Voices
that the rendered version of a saved SunVox project will be identical to the original.

First it runs two SunVox renders of the original project.
If there are differences here, the project has non-deterministic randomness,
and will not be further compared.

Next it will use SunVox to save the project to a file,
which will saved the SunVox-upgraded version of the project.
Then it will load and render that upgraded version, and compare it to the original.
If there are differences here, then there are issues with upgrading that project
that are outside the scope of Radiant Voices.

Finally, it will load the project into Radiant Voices, save that project,
then render that project and compare it to the original.
If there are differences here, then it means that Radiant Voices is not correctly
preserving the SunVox IFF structure.

At each stage, the tool will write out a `.hexdump.txt` file with an IFF hexdump
of the project file that is loaded and rendered.

Whenever there is an audio different, the tool will write out two `.wav` files.
One will be the difference between the original and the upgraded version.
The other will have a mono mixdown of the original on the left channel,
and a mono mixdown of the version being tested on the right channel.

Usage: python -m rv.tools.rendiff FILE
       python -m rv.tools.rendiff --help

Note: Before running, install the necessary packages::

    $ pip install -r requirements/tools.txt

You can run it across all SunVox examples using multiple cores:

    $ find . -name '*.sunvox' -print0 | xargs -0 -n 1 -P 8 python -m rv.tools.rendiff
"""

import argparse
import logging
import sys
from pathlib import Path

import rv.api
from rv.lib.iff import dump_file

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="SunVox to WAV file exporter")
parser.add_argument(
    "filename", metavar="FILE", type=str, nargs=1, help="SunVox file to export"
)

DATA_TYPE = None
FREQ = 44100
CHANNELS = 2


def main():
    global DATA_TYPE

    logging.basicConfig(level=logging.INFO)
    try:
        import numpy as np
        from scipy.io import wavfile
        from sunvox.api import Slot
        from sunvox.buffered import BufferedProcess, float32
        from tqdm import tqdm
    except ImportError:
        log.error(
            'Please "pip install -r requirements/tools.txt" '
            "to use sunvox.tools.export"
        )
        return 1

    DATA_TYPE = float32

    def process():
        return BufferedProcess(
            freq=FREQ,
            size=FREQ,
            channels=CHANNELS,
            data_type=DATA_TYPE,
        )

    def render(path):
        with process() as p:
            slot = Slot(path, process=p)
            length = slot.get_song_length_frames()
            output = np.zeros((length, 2), DATA_TYPE)
            position = 0
            slot.play_from_beginning()
            pbar = tqdm(total=length, unit_scale=True, unit="frame", dynamic_ncols=True)
            with pbar as pbar:
                while position < length:
                    buffer = p.fill_buffer()
                    end_pos = min(position + FREQ, length)
                    copy_size = end_pos - position
                    output[position:end_pos] = buffer[:copy_size]
                    position = end_pos
                    pbar.update(copy_size)
            log.info("Finished")
            return output

    def compare(audio1, audio2, diff_path, compare_path) -> bool:
        if not np.array_equal(audio1, audio2):
            log.warning("Found differences.")
            wavfile.write(diff_path, FREQ, audio1 - audio2)
            mixdown1 = audio1.transpose()[0] / 2 + audio1.transpose()[1] / 2
            mixdown2 = audio2.transpose()[0] / 2 + audio2.transpose()[1] / 2
            comparison = np.stack((mixdown1, mixdown2))
            wavfile.write(compare_path, FREQ, comparison.transpose())
            return True
        log.info("No differences found.")
        return False

    args = parser.parse_args()
    _in_filename = args.filename[0]
    in_path = Path(_in_filename)

    in_hexdump_path = in_path.with_suffix(".sunvox.hexdump.txt")
    log.info("Saving IFF hexdump of original SunVox file to %r", in_hexdump_path)
    with in_path.open("rb") as f, in_hexdump_path.open("w") as outfile:
        dump_file(f, outfile)

    resaved_path = in_path.with_suffix(".resaved.sunvox")
    log.info("Opening and re-saving project using SunVox to %r", resaved_path)
    with process() as resave_p:
        slot = Slot(str(in_path), process=resave_p)
        slot.save_filename(str(resaved_path))
    resaved_hexdump_path = resaved_path.with_suffix(".sunvox.hexdump.txt")
    log.info("Saving IFF hexdump of resaved SunVox file to %r", resaved_hexdump_path)
    with resaved_path.open("rb") as f, resaved_hexdump_path.open("w") as outfile:
        dump_file(f, outfile)

    log.info("Loading %s into rv", in_path)
    project = rv.api.read_sunvox_file(in_path)
    rv_path = in_path.with_suffix(".rv.sunvox")
    log.info("Saving RV-parsed project to %r", rv_path)
    with rv_path.open("wb") as f:
        project.write_to(f)
    rv_hexdump_path = rv_path.with_suffix(".sunvox.hexdump.txt")
    log.info("Saving IFF hexdump of RV-parsed SunVox file to %r", rv_hexdump_path)
    with rv_path.open("rb") as f, rv_hexdump_path.open("w") as outfile:
        dump_file(f, outfile)
    project.layout(scale=1024)
    layout_path = in_path.with_suffix(".rv.layout.sunvox")
    with layout_path.open("wb") as f:
        project.write_to(f)

    log.info("Rendering without rv preprocessing (pass 1/2)")
    output = render(in_path)

    log.info("Rendering without rv preprocessing (pass 2/2)")
    output2 = render(in_path)

    log.info("Comparing SunVox-only rendering")
    if compare(
        output,
        output2,
        in_path.with_suffix(".sunvox.diff.wav"),
        in_path.with_suffix(".sunvox.compare.wav"),
    ):
        return 1

    log.info("Rendering after SunVox-only resaving")
    output_resaved = render(resaved_path)

    log.info("Comparing SunVox-only rendering after resaving")
    if compare(
        output,
        output_resaved,
        resaved_path.with_suffix(".sunvox.diff.wav"),
        resaved_path.with_suffix(".sunvox.compare.wav"),
    ):
        return 1

    log.info("Rendering after RV saving")
    output_rv = render(project)

    log.info("Comparing original rendering with RV-parsed rendering")
    if compare(
        output,
        output_rv,
        rv_path.with_suffix(".sunvox.diff.wav"),
        rv_path.with_suffix(".sunvox.compare.wav"),
    ):
        return 1

    log.info("Successful comparison!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
