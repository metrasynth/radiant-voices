from struct import pack

from rv.container import Container


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
            raise ValueError('Cannot seriialize a synth with no module')
        yield self.MAGIC_CHUNK
        yield (b'VERS', pack('<I', self.sunsynth_version))
        module = self.module
        for chunk in module.iff_chunks():
            yield chunk
        for name in module.controllers:
            raw_value = module.get_raw(name)
            yield (b'CVAL', pack('<I', raw_value))
        if len(module.controllers) > 0:
            yield (b'CMID', b'\0\0\0\0\0\0\0\0' * len(module.controllers))
        yield (b'SEND', b'')
