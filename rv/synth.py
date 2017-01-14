from struct import pack

from rv.container import Container
from rv.errors import EmptySynthError


class Synth(Container):
    """SunSynth comprised of metadata and a single module

    A Synth can be saved as a ``.sunsynth`` file,
    or can be loaded into a project as a module.
    """

    MAGIC_CHUNK = (b'SSYN', b'')

    def __init__(self, module=None):
        self.sunsynth_version = 1
        self.module = module

    def chunks(self):
        """Generate chunks necessary to encode project as a .sunvox file"""
        if self.module is None:
            raise EmptySynthError('Cannot serialize a synth with no module')
        yield self.MAGIC_CHUNK
        yield (b'VERS', pack('<I', self.sunsynth_version))
        module = self.module
        for chunk in module.iff_chunks(in_project=False):
            yield chunk
        recompute = getattr(module, 'recompute_controller_attachment',
                            lambda: None)
        recompute()
        ctl_count = 0
        controllers = [(n, c) for n, c in module.controllers.items()
                       if c.attached(module)]
        for name, ctl in controllers:
            if ctl.attached(module):
                raw_value = module.get_raw(name)
                yield (b'CVAL', pack('<I', raw_value))
                ctl_count += 1
        if ctl_count:
            yield (b'CMID', b''.join(module.controller_midi_maps[name].cmid_data for name, _ in controllers))
        if module.chnk:
            yield (b'CHNK', pack('<I', max(0x10, module.chnk)))
            for chunk in module.specialized_iff_chunks():
                yield chunk
        yield (b'SEND', b'')
