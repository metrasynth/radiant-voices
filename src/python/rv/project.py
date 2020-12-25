from collections import namedtuple
from enum import IntEnum
from struct import pack
from typing import List, Optional

import networkx as nx
from rv import ENCODING
from rv.container import Container
from rv.errors import ModuleOwnershipError, PatternOwnershipError
from rv.modules.module import DisconnectingModule, Module
from rv.modules.output import Output
from rv.pattern import Pattern, PatternClone

PatternLine = namedtuple("PatternLine", ["index", "source", "line"])


class Project(Container):
    """SunVox project comprised of metadata, modules, and patterns

    A Project can be saved as a ``.sunvox`` file,
    or can be embedded within a `MetaModule`.
    """

    MAGIC_CHUNK = (b"SVOX", b"")

    class SyncCommand(IntEnum):
        start_stop = 1 << 0
        tempo = 1 << 1
        position = 1 << 2

    receive_sync_midi: SyncCommand
    receive_sync_other: SyncCommand

    modules: List[Optional[Module]]

    def __init__(self):
        self.modules = []
        self.output = Output()
        self.attach_module(self.output)
        self.sunvox_version = (1, 9, 6, 1)
        self.based_on_version = (1, 9, 6, 1)
        self.initial_bpm = 125
        self.initial_tpl = 6
        self.global_volume = 80
        self.name = "Project"
        self.time_grid = 4
        self.time_grid2 = 4
        self.metamodule = None
        self.modules_scale = 256
        self.modules_zoom = 256
        self.modules_x_offset = 0
        self.modules_y_offset = 0
        self.modules_layer_mask = 0x00000000
        self.modules_current_layer = 0
        self.timeline_position = 0
        self.restart_position = 0
        self.selected_module = 0
        self.selected_generator = 0
        self.current_pattern = 0
        self.current_track = 0
        self.current_line = 1
        self.receive_sync_midi = self.SyncCommand.start_stop
        self.receive_sync_other = self.SyncCommand.start_stop
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
        elif module.parent is not None and module.parent is not self:
            raise ModuleOwnershipError("Module is already attached to another project.")
        elif module not in self.modules:
            if None in self.modules:
                module.index = self.module_index(None)
                self.modules[module.index] = module
            else:
                self.modules.append(module)
                module.index = self.module_index(module)
            if isinstance(module, Output) and module.index == 0:
                self.output = module
            module.parent = self
        return module

    def attach_pattern(self, pattern):
        """Attach the pattern to the project."""
        if pattern.project is not None:
            raise PatternOwnershipError("Pattern already attached to a project")
        self.patterns.append(pattern)
        pattern.project = self
        return len(self.patterns) - 1

    def connect(self, from_modules, to_modules):
        """Make or break connections between modules."""
        if isinstance(from_modules, (DisconnectingModule, Module)):
            from_modules = [from_modules]
        if isinstance(to_modules, (DisconnectingModule, Module)):
            to_modules = [to_modules]
        for from_module in from_modules:
            for to_module in to_modules:
                disconnect = False
                if isinstance(from_module, DisconnectingModule):
                    disconnect = True
                    from_module = from_module.orig
                if isinstance(to_module, DisconnectingModule):
                    disconnect = True
                    to_module = to_module.orig
                try:
                    from_mod_idx = self.module_index(from_module)
                    to_mod_idx = self.module_index(to_module)
                except ValueError:
                    raise ModuleOwnershipError(
                        "Modules must have same parent to be connected or disconnected"
                    )
                in_links = to_module.in_links
                in_link_slots = to_module.in_link_slots
                out_links = from_module.out_links
                out_link_slots = from_module.out_link_slots
                if disconnect:
                    if from_mod_idx not in in_links:  # Already disconnected?
                        return
                    in_link_idx = in_links.index(from_mod_idx)
                    out_link_idx = out_links.index(to_mod_idx)
                    in_links[in_link_idx] = -1
                    out_links[out_link_idx] = -1
                    in_link_slots[in_link_idx] = -1
                    out_link_slots[out_link_idx] = -1
                    # [TODO] flatten to remove -1
                    return
                if from_mod_idx in in_links:  # Already connected?
                    return
                in_link_idx = len(in_links)
                in_links.append(from_mod_idx)
                out_link_idx = len(out_links)
                out_links.append(to_mod_idx)
                in_link_slots.append(out_link_idx)
                out_link_slots.append(in_link_idx)

    # [TODO] disconnect()
    # [TODO] replace_module(idx, new_module)

    def chunks(self):
        """Generate chunks necessary to encode project as a .sunvox file"""
        yield self.MAGIC_CHUNK
        yield b"VERS", pack("BBBB", *reversed(self.sunvox_version))
        yield b"BVER", pack("BBBB", *reversed(self.based_on_version))
        yield (
            b"SFGS",
            pack("<I", self.receive_sync_midi | (self.receive_sync_other << 3)),
        )
        yield b"BPM ", pack("<I", self.initial_bpm)
        yield b"SPED", pack("<I", self.initial_tpl)
        yield b"TGRD", pack("<I", self.time_grid)
        yield b"TGD2", pack("<I", self.time_grid2)
        yield b"GVOL", pack("<I", self.global_volume)
        yield b"NAME", self.name.encode(ENCODING) + b"\0"
        yield b"MSCL", pack("<I", self.modules_scale)
        yield b"MZOO", pack("<I", self.modules_zoom)
        yield b"MXOF", pack("<i", self.modules_x_offset)
        yield b"MYOF", pack("<i", self.modules_y_offset)
        yield b"LMSK", pack("<I", self.modules_layer_mask)
        yield b"CURL", pack("<I", self.modules_current_layer)
        yield b"TIME", pack("<i", self.timeline_position)
        if self.restart_position != 0:
            yield b"REPS", pack("<i", self.restart_position)
        yield b"SELS", pack("<I", self.selected_module)
        yield b"LGEN", pack("<I", self.selected_generator)
        yield b"PATN", pack("<I", self.current_pattern)
        yield b"PATT", pack("<I", self.current_track)
        yield b"PATL", pack("<I", self.current_line)
        for pattern in self.patterns:
            if pattern is not None:
                yield from pattern.iff_chunks()
            yield b"PEND", b""
        for i, module in enumerate(self.modules):
            if module is not None:
                yield from module.iff_chunks()
                links = module.in_links
                link_slots = module.in_link_slots
                if len(links) > 0:
                    structure = "<" + "i" * len(links)
                    links = pack(structure, *links)
                    link_slots = pack(structure, *link_slots)
                else:
                    links = b""
                    link_slots = b""
                yield b"SLNK", links
                yield b"SLnK", link_slots
                controllers = [
                    n for n, c in module.controllers.items() if c.attached(module)
                ]
                for name in controllers:
                    raw_value = module.get_raw(name)
                    yield b"CVAL", pack("<i", raw_value)
                if controllers:
                    yield (
                        b"CMID",
                        b"".join(
                            module.controller_midi_maps[name].cmid_data
                            for name in controllers
                        ),
                    )
                if module.chnk:
                    yield b"CHNK", pack("<I", module.chnk)
                    yield from module.specialized_iff_chunks()
            yield b"SEND", b""

    # def detach_module(self, module):
    #     """Detach a module from this project, disconnecting it from other modules."""
    #     if module.parent is not self or module not in self.modules:
    #         raise ModuleOwnershipError(
    #             "Cannot detach module not attached to this project"
    #         )
    #     disconnections = []
    #     for to_idx, from_idx_list in self.module_connections.items():
    #         if module.index == to_idx:
    #             for from_idx in from_idx_list:
    #                 disconnections.append(
    #                     (self.modules[from_idx], self.modules[to_idx])
    #                 )
    #         if module.index in from_idx_list:
    #             disconnections.append((module, self.modules[to_idx]))
    #     for from_idx, to_idx in disconnections:
    #         self.disconnect(from_idx, to_idx)
    #     self.modules[module.index] = None
    #     module.parent = None
    #     module.index = None
    #     return module

    # def disconnect(self, from_modules, to_modules):
    #     """Remove a connection from one module to another."""
    #     if isinstance(from_modules, Module):
    #         from_modules = [from_modules]
    #     if isinstance(to_modules, Module):
    #         to_modules = [to_modules]
    #     for from_module in from_modules:
    #         for to_module in to_modules:
    #             from_idx = self.module_index(from_module)
    #             to_idx = self.module_index(to_module)
    #             connections_to = self.module_connections[to_idx]
    #             connections_from = self.module_connections[from_idx]
    #             if from_idx in connections_to:
    #                 connections_to.remove(from_idx)
    #                 to_module.in_links = connections_to
    #             if to_idx in connections_from:
    #                 connections_from.remove(to_idx)
    #                 from_module.in_links = connections_from

    def pattern_lines(self, start=0, stop=None):
        """Yields information about the active pattern lines for each project line."""
        if len(self.patterns) == 0:
            return
        active_patterns = []
        activate_at = {}
        deactivate_at = {}
        for index, pattern in enumerate(
            sorted(self.patterns, key=lambda p: (p.y, p.x))
        ):
            if start <= pattern.x and (stop is None or pattern.x < stop):
                activate_at.setdefault(pattern.x, []).append((index, pattern))
                deactivate_at.setdefault(
                    pattern.x + pattern.source_pattern.lines, []
                ).append((index, pattern))
        for line in range(
            start, stop if stop is not None else max(deactivate_at.keys())
        ):
            for index, pattern in deactivate_at.get(line, []):
                active_patterns.remove((index, pattern))
            for index, pattern in activate_at.get(line, []):
                active_patterns.append((index, pattern))
            pattern_lines = [
                PatternLine(index, pattern.source or index, line - pattern.x)
                for index, pattern in active_patterns
            ]

            yield line, pattern_lines

    def layout(self, scale=512, **spring_layout_args):
        """Auto-layout modules."""
        g = nx.Graph()
        for module in self.modules:
            to_idx = module.index
            for from_idx in module.in_links:
                if from_idx >= 0:
                    g.add_nodes_from([from_idx, to_idx])
                    g.add_edge(from_idx, to_idx)
        pos = nx.spring_layout(g, scale=scale, **spring_layout_args)
        for idx, (x, y) in pos.items():
            mod = self.modules[idx]
            mod.x, mod.y = int(x), int(y)
        return True

    def module_index(self, module):
        """Return the index of the given module."""
        return self.modules.index(module)

    def new_module(self, cls, *args, **kw):
        """Construct and return a new module attached to this project."""
        mod = cls(*args, **kw)
        self.attach_module(mod)
        return mod

    def on_controller_changed(self, module, controller, value, down, up):
        if self.metamodule and up:
            self.metamodule.on_embedded_controller_changed(module, controller, value)
