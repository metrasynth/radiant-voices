import sys
import struct

from rv.reader.chunks import chunks
from rv.structure.conversions import base2_to_base10
from rv.structure.module import Module
from rv.structure.sunvoxfile import SunvoxFile


def read_sunvox_file(filename):
    with open(filename, 'rb') as f:
        reader = Reader(f)
        for chunk in chunks(f):
            reader.process(chunk)
        return reader.last


class Reader(object):

    def __init__(self, f):
        self.f = f
        self.objects = []
        self.current = None
        self.last = None

    def push(self, obj):
        self.objects.append(obj)
        self.last = self.current
        self.current = obj
        return obj

    def pop(self):
        popped = self.objects.pop()
        self.last = self.current
        self.current = self.objects[-1] if len(self.objects) else None
        return popped

    def process(self, chunk):
        chunk_name = chunk.getname().decode('ascii').lower().strip()
        if len(self.objects) == 0:
            class_name = 'initial'
        else:
            class_name = str(type(self.objects[-1]).__name__).lower()
        method_name = 'process_{}_{}'.format(class_name, chunk_name)
        method = getattr(self, method_name, None)
        if callable(method):
            method(chunk)
        else:
            print('--- NO HANDLER: {}({})'.format(method_name, chunk.read()))

    def process_initial_svox(self, chunk):
        """Project / Start"""
        self.push(SunvoxFile())
        
    def process_initial_send(self, chunk):
        """Extra SEND"""
        print('*** WARNING: Extra SEND')

    def process_sunvoxfile_vers(self, chunk):
        """Project / Version"""
        unpacked = struct.unpack('<BBBB', chunk.read())
        version = tuple(reversed(unpacked))
        self.current.project.sunvox_version = version
        print('    Sunvox version {}'.format(version))

    def process_sunvoxfile_bver(self, chunk):
        """Project / Based-on Version"""
        unpacked = struct.unpack('<BBBB', chunk.read())
        version = tuple(reversed(unpacked))
        self.current.project.based_on_version = version
        print('    Based on version {}'.format(version))

    def process_sunvoxfile_bpm(self, chunk):
        """Project / Initial BPM"""
        bpm, = struct.unpack('<I', chunk.read())
        self.current.project.initial_bpm = bpm
        print('    BPM {}'.format(bpm))

    def process_sunvoxfile_sped(self, chunk):
        """Project / Initial TPL"""
        tpl, = struct.unpack('<I', chunk.read())
        self.current.project.initial_tpl = tpl
        print('    TPL {}'.format(tpl))

    def process_sunvoxfile_gvol(self, chunk):
        """Project / Global Volume"""
        volume, = struct.unpack('<I', chunk.read())
        self.current.project.global_volume = volume
        print('    Global volume {} ({}%)'.format(volume, base2_to_base10(volume)))

    def process_sunvoxfile_name(self, chunk):
        """Project / Name"""
        name = chunk.read().rstrip(b'\0').decode('ascii')
        self.current.project.name = name
        print('    Name {!r}'.format(name))

    def process_sunvoxfile_mscl(self, chunk):
        """Project / Modules Scale"""
        scale, = struct.unpack('<I', chunk.read())
        self.current.project.modules_scale = scale
        print('    Modules scale {}'.format(scale))

    def process_sunvoxfile_mzoo(self, chunk):
        """Project / Modules Zoom"""
        zoom, = struct.unpack('<I', chunk.read())
        self.current.project.modules_zoom = zoom
        print('    Modules zoom {}'.format(zoom))

    def process_sunvoxfile_mxof(self, chunk):
        """Project / Modules X Offset"""
        offset, = struct.unpack('<i', chunk.read())
        self.current.project.modules_x_offset = offset
        print('    Modules X offset {}'.format(offset))

    def process_sunvoxfile_myof(self, chunk):
        """Project / Modules Y Offset"""
        offset, = struct.unpack('<i', chunk.read())
        self.current.project.modules_y_offset = offset
        print('    Modules Y offset {}'.format(offset))

    def process_sunvoxfile_lmsk(self, chunk):
        """Project / Modules Layer Mask"""
        layer_mask, = struct.unpack('<Bxxx', chunk.read())
        mask_list = [bool(layer_mask & (1 << x)) for x in range(8)]
        self.current.project.layer_mask = mask_list
        print('    Modules layer mask {}'.format(mask_list))

    def process_sunvoxfile_curl(self, chunk):
        """Project / Modules Current Layer"""
        current_layer, = struct.unpack('<Bxxx', chunk.read())
        self.current.project.current_layer = current_layer
        print('    Modules current layer {}'.format(current_layer))

    def process_sunvoxfile_sfff(self, chunk):
        """Module / Flags"""
        flags, = struct.unpack('<Bxxx', chunk.read())
        module = Module()
        module.flags = flags
        self.current.modules.append(module)
        self.push(module)
        print('    Module flags {:08b}'.format(flags))

    def process_sunvoxfile_send(self, chunk):
        """Project / End"""
        project = self.pop()
        print('    Project end ({!r})'.format(self.last))

    def process_module_snam(self, chunk):
        """Module / Name"""
        self.current.name = chunk.read().decode('ascii').rstrip('\0')
        print('    Module name {!r}'.format(self.current.name))

    def process_module_sfin(self, chunk):
        """Module / Finetune"""
        finetune, = struct.unpack('<i', chunk.read())
        self.current.finetune = finetune
        print('    Module finetune {}'.format(finetune))

    def process_module_srel(self, chunk):
        """Module / Relative Note"""
        relative_note, = struct.unpack('<i', chunk.read())
        self.current.relative_note = relative_note
        print('    Module relative note {}'.format(relative_note))

    def process_module_sxxx(self, chunk):
        """Module / X position"""
        x, = struct.unpack('<i', chunk.read())
        self.current.x = x
        print('    Module x {}'.format(x))

    def process_module_syyy(self, chunk):
        """Module / Y position"""
        y, = struct.unpack('<i', chunk.read())
        self.current.y = y
        print('    Module y {}'.format(y))

    def process_module_szzz(self, chunk):
        """Module / Z position (layer)"""
        z, = struct.unpack('<i', chunk.read())
        self.current.z = z
        print('    Module Z {}'.format(z))

    def process_module_scol(self, chunk):
        """Module / Color (R, G, B)"""
        color = struct.unpack('<BBB', chunk.read())
        self.current.color = color
        print('    Module color {}'.format(color))

    def process_module_slnk(self, chunk):
        """Module / Links (Out)"""
        if chunk.getsize() > 0:
            pass
        else:
            print('    Module link (NULL)')

    def process_module_sscl(self, chunk):
        """Module / Scale"""
        scale, = struct.unpack('<I', chunk.read())
        self.current.scale = scale
        print('    Module scale {}'.format(scale))

    def process_module_send(self, chunk):
        """Module / End"""
        self.pop()
        print('    Module end')
