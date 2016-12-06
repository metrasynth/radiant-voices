from rv.controller import Controller
from rv.modules import Behavior as B, Module


class DrumSynth(Module):

    name = mtype = 'DrumSynth'
    mgroup = 'Synth'

    behaviors = {B.receives_notes, B.sends_audio}

    volume = Controller((0, 512), 256)
    panning = Controller((-128, 128), 0)
    polyphony_ch = Controller((1, 8), 4)
    bass_volume = Controller((0, 512), 200)
    bass_power = Controller((0, 256), 256)
    bass_tone = Controller((0, 256), 64)
    bass_length = Controller((0, 256), 64)
    hihat_volume = Controller((0, 512), 256)
    hihat_length = Controller((0, 256), 64)
    snare_volume = Controller((0, 512), 256)
    snare_tone = Controller((0, 256), 128)
    snare_length = Controller((0, 256), 64)
