import logging
from collections import defaultdict
from struct import pack

from rv import ENCODING
from rv.container import Container
from rv.modules.module import Module
from rv.modules.output import Output
from rv.pattern import Pattern, PatternClone

try:
    import pygraphviz as pgv
except ImportError:
    pgv = None


class Project(Container):
    """SunVox project comprised of metadata, modules, and patterns

    A Project can be saved as a ``.sunvox`` file,
    or can be embedded within a `MetaModule`.
    """

    MAGIC_CHUNK = (b'SVOX', b'')

    def __init__(self):
        self.modules = []
        self.module_connections = defaultdict(list)
        self.output = Output()
        self.attach_module(self.output)
        self.sunvox_version = (1, 9, 2, 0)
        self.based_on_version = (1, 9, 2, 0)
        self.initial_bpm = 125
        self.initial_tpl = 6
        self.global_volume = 80
        self.name = 'Project'
        self.time_grid = 4
        self.metamodule = None
        self.modules_scale = 256
        self.modules_zoom = 256
        self.modules_x_offset = 0
        self.modules_y_offset = 0
        self.modules_layer_mask = 0x00000000
        self.modules_current_layer = 0
        self.timeline_position = 0
        self.selected_module = 0
        self.current_pattern = 0
        self.current_track = 0
        self.current_line = 1
        self.patterns = []

    def __iadd__(self, other):
        if isinstance(other, list):
            for x in other:
                self.__iadd__(x)
        elif isinstance(other, Module):
            self.attach_module(other)
        elif isinstance(other, (Pattern, PatternClone)):
            self.attach_pattern(other)
        return self

    def attach_module(self, module):
        """Attach the module to the project."""
        if module is None:
            self.modules.append(module)
        elif module not in self.modules:
            self.modules.append(module)
            module.index = self.module_index(module)
            if isinstance(module, Output) and module.index == 0:
                self.output = module
            self.module_connections[module.index] = module.incoming_links
            module.parent = self
        return module

    def attach_pattern(self, pattern):
        """Attach the pattern to the project."""
        self.patterns.append(pattern)

    def connect(self, from_modules, to_modules):
        """Establish a connection from module(s) to another module(s)."""
        if isinstance(from_modules, Module):
            from_modules = [from_modules]
        if isinstance(to_modules, Module):
            to_modules = [to_modules]
        for from_module in from_modules:
            for to_module in to_modules:
                from_idx = self.module_index(from_module)
                to_idx = self.module_index(to_module)
                connections_to = self.module_connections[to_idx]
                connections_from = self.module_connections[from_idx]
                connected = (
                    from_idx in connections_to
                    or to_idx in connections_from
                )
                if not connected:
                    connections_to.append(from_idx)
                    to_module.incoming_links = connections_to

    def chunks(self):
        """Generate chunks necessary to encode project as a .sunvox file"""
        yield self.MAGIC_CHUNK
        yield (b'VERS', pack('BBBB', *reversed(self.sunvox_version)))
        yield (b'BVER', pack('BBBB', *reversed(self.based_on_version)))
        yield (b'BPM ', pack('<I', self.initial_bpm))
        yield (b'SPED', pack('<I', self.initial_tpl))
        yield (b'TGRD', pack('<I', self.time_grid))
        yield (b'GVOL', pack('<I', self.global_volume))
        yield (b'NAME', self.name.encode(ENCODING) + b'\0')
        yield (b'MSCL', pack('<I', self.modules_scale))
        yield (b'MZOO', pack('<I', self.modules_zoom))
        yield (b'MXOF', pack('<i', self.modules_x_offset))
        yield (b'MYOF', pack('<i', self.modules_y_offset))
        yield (b'LMSK', pack('<I', self.modules_layer_mask))
        yield (b'CURL', pack('<I', self.modules_current_layer))
        yield (b'TIME', pack('<i', self.timeline_position))
        yield (b'SELS', pack('<I', self.selected_module))
        yield (b'LGEN', getattr(self, '_reader_lgen', b'\x01\0\0\0'))  # ???
        yield (b'PATN', pack('<I', self.current_pattern))
        yield (b'PATT', pack('<I', self.current_track))
        yield (b'PATL', pack('<I', self.current_line))
        for pattern in self.patterns:
            if pattern is not None:
                for chunk in pattern.iff_chunks():
                    yield chunk
            yield (b'PEND', b'')
        for i, module in enumerate(self.modules):
            if module is not None:
                for chunk in module.iff_chunks():
                    yield chunk
                connections = self.module_connections[i]
                if len(connections) > 0:
                    connections.append(-1)
                    structure = '<' + 'i' * len(connections)
                    links = pack(structure, *connections)
                else:
                    links = b''
                yield (b'SLNK', links)
                controllers = [n for n, c in module.controllers.items()
                               if c.attached(module)]
                for name in controllers:
                    raw_value = module.get_raw(name)
                    yield (b'CVAL', pack('<I', raw_value))
                if len(controllers) > 0:
                    yield (b'CMID', b''.join(module.controller_midi_maps[name].cmid_data for name in controllers))
                if module.chnk:
                    yield (b'CHNK', pack('<I', max(0x10, module.chnk)))
                    for chunk in module.specialized_iff_chunks():
                        yield chunk
            yield (b'SEND', b'')

    def disconnect(self, from_modules, to_modules):
        """Remove a connection from one module to another."""
        if isinstance(from_modules, Module):
            from_modules = [from_modules]
        if isinstance(to_modules, Module):
            to_modules = [to_modules]
        for from_module in from_modules:
            for to_module in to_modules:
                from_idx = self.module_index(from_module)
                to_idx = self.module_index(to_module)
                connections_to = self.module_connections[to_idx]
                connections_from = self.module_connections[from_idx]
                if from_idx in connections_to:
                    connections_to.remove(from_idx)
                    to_module.incoming_links = connections_to
                if to_idx in connections_from:
                    connections_from.remove(to_idx)
                    from_module.incoming_links = connections_from

    def graph(self):
        """Return a PyGraphViz-compatible graph dictionary for modules."""
        d = defaultdict(list)
        for to_idx, from_idx_list in self.module_connections.items():
            for from_idx in from_idx_list:
                if from_idx >= 0:
                    d[from_idx].append(to_idx)
        return d

    def layout(self, prog='dot', factor=8, offset=0):
        """Use GraphViz to auto-layout modules."""
        if pgv is not None:
            g = pgv.AGraph(self.graph(), directed=True, strict=False)
            g.layout(prog=prog)
            for node in g.nodes():
                x, y = node.attr['pos'].split(',')
                x, y = int(float(x)), int(float(y))
                idx = int(node)
                mod = self.modules[idx]
                if isinstance(factor, int):
                    xfactor, yfactor = factor, factor
                else:
                    xfactor, yfactor = factor
                if isinstance(offset, int):
                    xoffset, yoffset = offset, offset
                else:
                    xoffset, yoffset = offset
                mod.x = x * xfactor + xoffset
                mod.y = y * yfactor + yoffset
            return True
        else:
            logging.warning('GraphViz not available; could not auto-layout.')
            return False

    def module_index(self, module):
        """Return the index of the given module."""
        return self.modules.index(module)

    def new_module(self, cls, *args, **kw):
        """Construct and return a new module attached to this project."""
        module = cls(*args, **kw)
        self.attach_module(module)
        return module

    def on_controller_changed(self, module, controller, value, down, up):
        if self.metamodule and up:
            self.metamodule.on_embedded_controller_changed(
                module, controller, value)
