import logging
from logutils import BraceMessage as _F
log = logging.getLogger(__name__)

import struct

from hexdump import hexdump

from rv import ENCODING
from rv.lib.conversions import base2_to_base10
from rv.lib.iff import chunks
from rv.project import Project


def read_sunvox_file(file_or_name):
    from rv.readers.initial import InitialReader
    close = False
    if isinstance(file_or_name, str):
        file_or_name = open(file_or_name, 'rb')
        close = True
    try:
        reader = InitialReader(file_or_name)
        return reader.object
    finally:
        if close:
            file_or_name.close()


class Reader(object):
    """Abstract base class for reading SunVox and SunSynth IFF files"""

    def __init__(self, f):
        self.f = f
        self._object = None

    @property
    def object(self):
        if self._object is None:
            self.process_chunks()
        return self._object

    @object.setter
    def object(self, value):
        if self._object is None:
            self._object = value
        else:
            raise AttributeError('object was already set')

    def process_chunks(self):
        try:
            for name, data in chunks(self.f):
                name = name.decode(ENCODING).strip().lower()
                method_name = 'process_{}'.format(name)
                method = getattr(self, method_name, None)
                log_args = (self.__class__.__name__, method_name)
                if callable(method):
                    log.debug(_F('-> {}.{}', *log_args))
                    method(data)
                else:
                    log.warn(_F('no {}.{} method', *log_args))
            self.process_end_of_file()
        except ReaderFinished:
            pass

    def rewind(self, data):
        new_pos = self.f.tell() - len(data) - 8
        self.f.seek(new_pos)

    def process_end_of_file(self):
        raise RuntimeError('Reached end of file without a handler')


class ReaderFinished(Exception):
    """A reader is finished processing its relevant chunks."""


class OldReader(object):

    def __init__(self, f):
        self.f = f
        self.project = Project()
        self.objects = []
        self.current = None
        self.last = None
        self.top = None
        self.last_chunk_name = None
        for chunk in chunks(f):
            self.process(chunk)
        self.specialize_modules()

    def _log_message(self, message):
        """Indent log message according to object depth"""
        indent = '  ' * len(self.objects)
        return '{}({:>12s}/{:4s}) {}'.format(
            indent, self.current_class_name,
            self.last_chunk_name.upper(), message)

    def debug(self, message, *args, **kw):
        log.debug(_F(self._log_message(message), *args, **kw))

    def warn(self, message, *args, **kw):
        log.warn(_F(self._log_message(message), *args, **kw))

    def push(self, obj):
        self.objects.append(obj)
        self.last = self.current
        self.current = obj
        if self.top is None:
            self.top = obj
        return obj

    def pop(self):
        popped = self.objects.pop()
        self.last = self.current
        self.current = self.objects[-1] if len(self.objects) else None
        return popped

    @property
    def current_class_name(self):
        if self.current is None:
            return 'initial'
        else:
            return str(type(self.current).__name__).lower()

    def process(self, chunk):
        chunk_name = chunk.getname().decode(ENCODING).lower().strip()
        class_name = self.current_class_name
        self.last_chunk_name = chunk_name
        method_name = 'process_{}_{}'.format(class_name, chunk_name)
        method = getattr(self, method_name, None)
        if callable(method):
            method(chunk)
        else:
            data = chunk.read()
            if len(data) == 4:
                value, = struct.unpack('<i', data)
                uvalue, = struct.unpack('<I', data)
                self.warn('no handler for {0}({1} '
                          '[signed {2:d} {2:#x} {2:#b}] '
                          '[unsigned {3:d} {3:#x} {3:#b}])',
                          method_name, data, value, uvalue)
            else:
                self.warn('no handler for {}({} bytes)\n{}', method_name,
                          len(data), hexdump(data, 'return'))

    def specialize_modules(self):
        if hasattr(self.top, 'modules'):
            self.top._modules = [m.specialized() if m is not None else None
                                 for m in self.top.modules]

    def process_initial_svox(self, _):
        """Project / Start"""
        self.debug('sunvox file start')
        self.push(SunvoxFile())

    def process_initial_ssyn(self, _):
        """Synth / Start"""
        self.debug('sunsynth file start')
        self.push(SunsynthFile())

    def process_initial_send(self, _):
        """Empty module"""
        self.debug('empty module {:#04x}', len(self.current._modules))
        self.current._modules.append(None)

    process_sunvoxfile_send = process_initial_send

    def process_sunvoxfile_vers(self, chunk):
        """Project / Version"""
        unpacked = struct.unpack('BBBB', chunk.read())
        version = tuple(reversed(unpacked))
        self.current.project.sunvox_version = version
        self.debug('sunvox_version = {}', version)

    process_sunsynthfile_vers = process_sunvoxfile_vers

    def process_sunvoxfile_bver(self, chunk):
        """Project / Based-on Version"""
        unpacked = struct.unpack('BBBB', chunk.read())
        version = tuple(reversed(unpacked))
        self.current.project.based_on_version = version
        self.debug('based_on_version = {}', version)

    def process_sunvoxfile_bpm(self, chunk):
        """Project / Initial BPM"""
        bpm, = struct.unpack('<I', chunk.read())
        self.current.project.initial_bpm = bpm
        self.debug('initial_bpm = {}', bpm)

    def process_sunvoxfile_sped(self, chunk):
        """Project / Initial TPL"""
        tpl, = struct.unpack('<I', chunk.read())
        self.current.project.initial_tpl = tpl
        self.debug('initial_tpl = {}', tpl)

    def process_sunvoxfile_gvol(self, chunk):
        """Project / Global Volume"""
        volume, = struct.unpack('<I', chunk.read())
        self.current.project.global_volume = volume
        self.debug('global_volume = {} ({}%)', volume, base2_to_base10(volume))

    def process_sunvoxfile_name(self, chunk):
        """Project / Name"""
        name = chunk.read().rstrip(b'\0').decode(ENCODING)
        self.current.project.name = name
        self.debug('name = {!r}', name)

    def process_sunvoxfile_mscl(self, chunk):
        """Project / Modules Scale"""
        scale, = struct.unpack('<I', chunk.read())
        self.current.project.modules_scale = scale
        self.debug('modules_scale = {}', scale)

    def process_sunvoxfile_mzoo(self, chunk):
        """Project / Modules Zoom"""
        zoom, = struct.unpack('<I', chunk.read())
        self.current.project.modules_zoom = zoom
        self.debug('modules_zoom = {}', zoom)

    def process_sunvoxfile_mxof(self, chunk):
        """Project / Modules X Offset"""
        offset, = struct.unpack('<i', chunk.read())
        self.current.project.modules_x_offset = offset
        self.debug('modules_x_offset = {}', offset)

    def process_sunvoxfile_myof(self, chunk):
        """Project / Modules Y Offset"""
        offset, = struct.unpack('<i', chunk.read())
        self.current.project.modules_y_offset = offset
        self.debug('modules_y_offset = {}', offset)

    def process_sunvoxfile_lmsk(self, chunk):
        """Project / Modules Layer Mask"""
        layer_mask, = struct.unpack('<I', chunk.read())
        self.current.project.layer_mask = layer_mask
        self.debug('layer_mask = {:#010b}', layer_mask)

    def process_sunvoxfile_curl(self, chunk):
        """Project / Modules Current Layer"""
        current_layer, = struct.unpack('<I', chunk.read())
        self.current.project.current_layer = current_layer
        self.debug('current_layer = {}', current_layer)

    def process_sunvoxfile_time(self, chunk):
        """Project / Timeline Position"""
        current_time, = struct.unpack('<i', chunk.read())
        self.current.project.timeline_position = current_time
        self.debug('timeline_position = {}', current_time)

    def process_sunvoxfile_sels(self, chunk):
        """Project / Selected Module"""
        selected, = struct.unpack('<I', chunk.read())
        self.current.project.selected_module = selected
        self.debug('selected_module = {:#04x}', selected)

    def process_sunvoxfile_patn(self, chunk):
        """Project / Pattern number being edited"""
        pattern, = struct.unpack('<I', chunk.read())
        self.current.project.current_pattern = pattern
        self.debug('current_pattern = {:#06x}', pattern)

    def process_sunvoxfile_patt(self, chunk):
        """Project / Pattern track being edited"""
        track, = struct.unpack('<I', chunk.read())
        self.current.project.current_track = track
        self.debug('current_track = {:#04x} ({})', track, track)

    def process_sunvoxfile_patl(self, chunk):
        """Project / Pattern line being edited"""
        line, = struct.unpack('<I', chunk.read())
        self.current.project.current_line = line
        self.debug('current_line = {:#04x} ({})', line, line)

    def process_sunvoxfile_pdta(self, chunk):
        """Pattern / Data"""
        data = chunk.read()
        pattern = Pattern()
        pattern.data = data
        self.debug('pattern start {:#06x}'.format(len(self.current._patterns)))
        self.current._patterns.append(pattern)
        self.push(pattern)
        self.debug('data = ({} bytes)', len(data))

    def process_sunvoxfile_sfff(self, chunk):
        """Module / Flags"""
        flags, = struct.unpack('<I', chunk.read())
        module = Module()
        module.flags = flags
        self.debug('module start {:#06x}', len(self.current._modules))
        self.current._modules.append(module)
        self.push(module)
        self.debug('flags = {:#010b}', flags)

    process_sunsynthfile_sfff = process_sunvoxfile_sfff

    def process_pattern_pxxx(self, chunk):
        """Pattern / X position"""
        x, = struct.unpack('<i', chunk.read())
        self.current.x = x
        self.debug('x = {}', x)

    def process_pattern_pyyy(self, chunk):
        """Pattern / Y position"""
        y, = struct.unpack('<i', chunk.read())
        self.current.y = y
        self.debug('y = {}', y)

    def process_pattern_pfgc(self, chunk):
        """Pattern / Foreground color"""
        color = struct.unpack('BBB', chunk.read())
        self.current.fg_color = color
        self.debug('fg_color = {}', color)

    def process_pattern_pbgc(self, chunk):
        """Pattern / Background color"""
        color = struct.unpack('BBB', chunk.read())
        self.current.bg_color = color
        self.debug('bg_color = {}', color)

    def process_pattern_pfff(self, chunk):
        """Pattern / Selection Flags"""
        flags, = struct.unpack('<I', chunk.read())
        self.current.selection_flags = flags
        self.current.selected = bool(flags & 0b10)
        self.debug('selection_flags = {:#010b}', flags)
        self.debug('is_selected == {}', self.current.is_selected)

    def process_pattern_pflg(self, chunk):
        """Pattern / Property Flags"""
        flags, = struct.unpack('<I', chunk.read())
        self.current.property_flags = flags
        self.debug('property_flags = {:#010b}', flags)
        self.debug('has_no_icon == {}', self.current.has_no_icon)

    def process_pattern_pico(self, chunk):
        """Pattern / Icon"""
        icon = chunk.read()
        self.current.icon = icon
        self.debug('icon = ({} bytes)', len(icon))

    def process_pattern_plin(self, chunk):
        """Pattern / Lines"""
        lines, = struct.unpack('<I', chunk.read())
        self.current.lines = lines
        self.debug('lines = {}', lines)

    def process_pattern_pend(self, _):
        self.pop()
        self.debug('pattern end {:#06x}', len(self.current._patterns) - 1)

    def process_module_snam(self, chunk):
        """Module / Name"""
        self.current.name = chunk.read().decode(ENCODING).rstrip('\0')
        self.debug('name = {!r}', self.current.name)

    def process_module_styp(self, chunk):
        """Module / Type"""
        self.current.type = chunk.read().decode(ENCODING).rstrip('\0')
        self.debug('type = {!r}', self.current.type)

    def process_module_sfin(self, chunk):
        """Module / Finetune"""
        finetune, = struct.unpack('<i', chunk.read())
        self.current.finetune = finetune
        self.debug('finetune = {}', finetune)

    def process_module_srel(self, chunk):
        """Module / Relative Note"""
        relative_note, = struct.unpack('<i', chunk.read())
        self.current.relative_note = relative_note
        self.debug('relative_note = {}', relative_note)

    def process_module_sxxx(self, chunk):
        """Module / X position"""
        x, = struct.unpack('<i', chunk.read())
        self.current.x = x
        self.debug('x = {}', x)

    def process_module_syyy(self, chunk):
        """Module / Y position"""
        y, = struct.unpack('<i', chunk.read())
        self.current.y = y
        self.debug('y = {}', y)

    def process_module_szzz(self, chunk):
        """Module / Z position (layer)"""
        z, = struct.unpack('<i', chunk.read())
        self.current.z = z
        self.debug('z = {}', z)

    def process_module_scol(self, chunk):
        """Module / Color (R, G, B)"""
        color = struct.unpack('BBB', chunk.read())
        self.current.color = color
        self.debug('color = {}', color)

    def process_module_slnk(self, chunk):
        """Module / Links (Out)"""
        if chunk.getsize() > 0:
            links = []
            while True:
                index = len(links)
                data = chunk.read(4)
                if len(data) == 0:
                    break
                source, = struct.unpack('<i', data)
                if source > -1:
                    links.append(source)
                    self.debug('incoming_links[{}] = {:#04x}', index, source)
                else:
                    break
            self.current.incoming_links = links
        else:
            self.debug('(no incoming links)')

    def process_module_sscl(self, chunk):
        """Module / Scale"""
        scale, = struct.unpack('<I', chunk.read())
        self.current.scale = scale
        self.debug('scale = {}', scale)

    def process_module_smic(self, chunk):
        """Module / Midi Out Channel"""
        channel, = struct.unpack('<I', chunk.read())
        self.current.midi_out_channel = channel
        self.debug('midi_out_channel = {}', channel)

    def process_module_smin(self, chunk):
        """Module / Midi Out Name"""
        name = chunk.read().decode(ENCODING).rstrip('\0')
        self.current.midi_out_name = name
        self.debug('midi_out_name = {!r}', name)

    def process_module_smib(self, chunk):
        """Module / Midi Out Bank"""
        bank, = struct.unpack('<i', chunk.read())
        self.current.midi_out_bank = bank
        self.debug('midi_out_bank = {}', bank)

    def process_module_smip(self, chunk):
        """Module / Midi Out Program"""
        program, = struct.unpack('<i', chunk.read())
        self.current.midi_out_program = program
        self.debug('midi_out_program = {}', program)

    def process_module_cval(self, chunk):
        """Module / Controller Value"""
        value, = struct.unpack('<i', chunk.read())
        index = len(self.current.controller_values)
        self.current.controller_values.append(value)
        self.debug('controller_values[{}] = {} ({:#06x})', index, value, value)

    def process_module_cmid(self, chunk):
        """Module / Controller MIDI Inputs

        Requires `process_module_cval` to have been processed.
        """
        for i in range(len(self.current.controller_values)):
            data = chunk.read(8)
            self.debug('controller_midi_inputs[{}] = {!r}', i, data)
            self.current.midi_inputs.append(data)

    def process_module_svpr(self, chunk):
        params, = struct.unpack('<I', chunk.read())
        self.current.visualization_params = params
        self.debug('visualization_params = {:#010x}', params)

    def process_module_send(self, _):
        """Module / End"""
        self.pop()
        self.debug('module end {:#04x}', len(self.current._modules) - 1)

    # TODO: process_module_svpr: visualization parameters
