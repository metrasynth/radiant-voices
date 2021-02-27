"""Render difference between rv-processed and native SunVox playback.

Usage: python -m rv.tools.rendiff FILE
       python -m rv.tools.rendiff --help

Note: Before running, install the necessary packages::

    $ pip install -r requirements/tools.txt
"""

import argparse
import logging
import os
import sys

import rv.api

log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description="SunVox to WAV file exporter")
parser.add_argument(
    "filename", metavar="FILE", type=str, nargs=1, help="SunVox file to export"
)


def main():
    logging.basicConfig(level=logging.INFO)
    try:
        import numpy as np
        from scipy.io import wavfile
        from sunvox import Slot
        from sunvox.buffered import BufferedProcess, float32
        from tqdm import tqdm
    except ImportError:
        log.error(
            'Please "pip install -r requirements/tools.txt" '
            "to use sunvox.tools.export"
        )
        return 1
    args = parser.parse_args()
    in_filename = args.filename[0]
    log.debug("Loading into rv")
    project = rv.api.read_sunvox_file(in_filename)
    root, ext = os.path.splitext(in_filename)
    out_filename = "{}.diff.wav".format(root)
    out2_filename = "{}.compare.wav".format(root)
    rv_filename = "{}.rv.sunvox".format(root)
    data_type = float32
    freq = 44100
    channels = 2

    log.info("Rendering without rv preprocessing (pass 1/2)")
    p = BufferedProcess(freq=freq, size=freq, channels=channels, data_type=data_type)
    slot = Slot(in_filename, process=p)
    length = slot.get_song_length_frames()
    output = np.zeros((length, 2), data_type)
    position = 0
    slot.play_from_beginning()
    pbar = tqdm(total=length, unit_scale=True, unit="frame", dynamic_ncols=True)
    with pbar as pbar:
        while position < length:
            buffer = p.fill_buffer()
            end_pos = min(position + freq, length)
            copy_size = end_pos - position
            output[position:end_pos] = buffer[:copy_size]
            position = end_pos
            pbar.update(copy_size)
    log.info("Finished")

    log.info("Rendering without rv preprocessing (pass 2/2)")
    p2 = BufferedProcess(freq=freq, size=freq, channels=channels, data_type=data_type)
    slot = Slot(in_filename, process=p2)
    length = slot.get_song_length_frames()
    output2 = np.zeros((length, 2), data_type)
    position = 0
    slot.play_from_beginning()
    pbar = tqdm(total=length, unit_scale=True, unit="frame", dynamic_ncols=True)
    with pbar as pbar:
        while position < length:
            buffer = p2.fill_buffer()
            end_pos = min(position + freq, length)
            copy_size = end_pos - position
            output2[position:end_pos] = buffer[:copy_size]
            position = end_pos
            pbar.update(copy_size)
    log.info("Finished")

    if not np.array_equal(output, output2):
        log.warning("Found differences using SunVox-only rendering.")
        p.kill()
        p2.kill()
        return 1

    log.info("Rendering with rv preprocessing")
    p3 = BufferedProcess(freq=freq, size=freq, channels=channels, data_type=data_type)
    slot = Slot(project, process=p3)
    length = slot.get_song_length_frames()
    output_rv = np.zeros((length, 2), data_type)
    position = 0
    slot.play_from_beginning()
    pbar = tqdm(total=length, unit_scale=True, unit="frame", dynamic_ncols=True)
    with pbar as pbar:
        while position < length:
            buffer = p3.fill_buffer()
            end_pos = min(position + freq, length)
            copy_size = end_pos - position
            output_rv[position:end_pos] = buffer[:copy_size]
            position = end_pos
            pbar.update(copy_size)
    log.info("Finished")

    log.info("Comparing")
    diff = output - output_rv
    if np.sum(np.abs(diff)) == 0:
        log.info("No differences found")
    else:
        log.info("Saving differences to %r", out_filename)
        wavfile.write(out_filename, freq, diff)
        log.info("Saving comparison to %r", out2_filename)
        sv_left, sv_right = output.transpose()
        sv_mixdown = sv_left / 2 + sv_right / 2
        rv_left, rv_right = output_rv.transpose()
        rv_mixdown = rv_left / 2 + rv_right / 2
        comparison = np.stack((sv_mixdown, rv_mixdown))
        wavfile.write(out2_filename, freq, comparison.transpose())
        log.info("Saving rv version to %r", rv_filename)
        with open(rv_filename, "wb") as f:
            project.write_to(f)
    log.info("Finished")

    p.kill()
    p2.kill()
    p3.kill()


if __name__ == "__main__":
    sys.exit(main())
