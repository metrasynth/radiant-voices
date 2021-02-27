from struct import pack

from rv.container import Container
from rv.errors import EmptySynthError


class Synth(Container):
    """SunSynth comprised of metadata and a single module

    A Synth can be saved as a ``.sunsynth`` file,
    or can be loaded into a project as a module.
    """

    MAGIC_CHUNK = (b"SSYN", b"")

    def __init__(self, module=None):
        self.sunsynth_version = (1, 9, 6, 1)
        self.module = module

    def chunks(self):
        """Generate chunks necessary to encode project as a .sunvox file"""
        if self.module is None:
            raise EmptySynthError("Cannot serialize a synth with no module")
        yield self.MAGIC_CHUNK
        yield b"VERS", pack("BBBB", *reversed(self.sunsynth_version))
        mod = self.module
        yield from mod.iff_chunks(in_project=False)
        recompute = getattr(mod, "recompute_controller_attachment", lambda: None)
        recompute()
        ctl_count = 0
        controllers = [(n, c) for n, c in mod.controllers.items() if c.attached(mod)]
        for name, ctl in controllers:
            if ctl.attached(mod):
                raw_value = mod.get_raw(name)
                yield b"CVAL", pack("<i", raw_value)
                ctl_count += 1
        if ctl_count:
            yield (
                b"CMID",
                b"".join(
                    mod.controller_midi_maps[name].cmid_data for name, _ in controllers
                ),
            )
        if mod.chnk:
            yield b"CHNK", pack("<I", mod.chnk)
            yield from mod.specialized_iff_chunks()
        yield b"SEND", b""
