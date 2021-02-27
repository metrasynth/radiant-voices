from copy import deepcopy
from enum import IntEnum
from struct import pack

from attr import attr, attributes
from rv import ENCODING
from rv.lib.validators import in_range, is_length
from rv.note import ALL_NOTES, NOTECMD, Note


class PatternAppearanceFlags(IntEnum):

    no_icon = 0x01


class PatternFlags(IntEnum):

    clone = 0x01
    selected = 0x02
    mute = 0x08
    solo = 0x10


@attributes
class Pattern:

    name = attr(None)
    tracks = attr(validator=in_range(1, 32), default=4)
    lines = attr(validator=in_range(1, 2 ** 19), default=32)
    y_size = attr(default=32)
    appearance_flags = attr(default=0)
    icon = attr(default=b"\0" * 32, validator=is_length(32))
    fg_color = attr(default=(0, 0, 0))
    bg_color = attr(default=(255, 255, 255))
    flags = attr(default=0)
    x = attr(default=0)
    y = attr(default=0)
    project = attr(default=None)
    source = None

    @property
    def data(self):
        if not hasattr(self, "_data"):
            self.clear()
        return self._data

    @property
    def raw_data(self):
        return b"".join(b"".join(note.raw_data for note in line) for line in self.data)

    @raw_data.setter
    def raw_data(self, raw_data):
        data = self.data
        for line_no in range(self.lines):
            for track_no in range(self.tracks):
                offset = (line_no * self.tracks * 8) + (track_no * 8)
                note_raw_data = raw_data[offset : offset + 8]
                data[line_no][track_no].raw_data = note_raw_data

    def set_via_fn(self, fn):
        """Set pattern contents by calling fn for each note.

        fn is called with this pattern, the line of the note, and the track of the note.
        It is expected to return a Note, which is replaced at the same location.

        The entirety of the original pattern data is kept until all notes
        have been processed successfully; only then do the new notes become
        part of the pattern.
        """
        new = deepcopy(self.data)
        for line in range(self.lines):
            for track in range(self.tracks):
                new[line][track] = fn(self, line, track)
        self._data = new
        return self

    def set_via_gen(self, gen):
        """Set pattern contents by receiving notes from a generator.

        gen is called with this pattern, and the new note data array.
        The generator then yields (line, track, Note-instance) tuples.

        It is possible, but *discouraged*, to directly change the new note array.
        It is passed in so that algorithms can reference the intermediate state
        of the pattern before committing.

        The generator must stop iteration at some point, or this method will
        never return.
        """
        new = deepcopy(self.data)
        for line, track, note in gen(self, new):
            new[line][track] = note
        self._data = new
        return self

    def iff_chunks(self):
        yield b"PDTA", self.raw_data
        if self.name is not None:
            yield b"PNME", self.name.encode(ENCODING) + b"\0"
        yield b"PCHN", pack("<I", self.tracks)
        yield b"PLIN", pack("<I", self.lines)
        yield b"PYSZ", pack("<I", self.y_size)
        yield b"PFLG", pack("<I", self.appearance_flags)
        yield b"PICO", self.icon
        yield b"PFGC", pack("<BBB", *self.fg_color)
        yield b"PBGC", pack("<BBB", *self.bg_color)
        yield b"PFFF", pack("<I", self.flags)
        yield b"PXXX", pack("<i", self.x)
        yield b"PYYY", pack("<i", self.y)

    def clear(self):
        self._data = []
        for line_no in range(self.lines):
            line = []
            self._data.append(line)
            for _ in range(self.tracks):
                line.append(Note(pattern=self))

    def tabular_repr(self, note_format="NN VV MMMM CC EE XXYY"):
        lines = []
        notes_on = [False] * self.tracks
        lineno_len = max(2, len(str(self.lines)))
        lineno_fmt = "{:0" + str(lineno_len) + "d}"
        for lineno, line in enumerate(self.data):
            notes = []
            lines.append((lineno_fmt.format(lineno), notes))
            for track_no, note in enumerate(line):
                if note.note in ALL_NOTES:
                    notes_on[track_no] = True
                elif note.note == NOTECMD.NOTE_OFF:
                    notes_on[track_no] = False
                notes.append(note.tabular_repr(notes_on[track_no], note_format))
        return "\n".join(
            [" | ".join([" " * lineno_len] + [note_format] * self.tracks)]
            + [" | ".join([lineno] + [n for n in notes]) for lineno, notes in lines]
        )

    @property
    def source_pattern(self):
        return self


@attributes
class PatternClone:

    source = attr()
    flags = attr(default=PatternFlags.clone)
    x = attr(default=0)
    y = attr(default=0)
    project = attr(default=None)

    def iff_chunks(self):
        yield b"PPAR", pack("<I", self.source)
        yield b"PFFF", pack("<I", self.flags)
        yield b"PXXX", pack("<i", self.x)
        yield b"PYYY", pack("<i", self.y)

    @property
    def source_pattern(self):
        return self.project.patterns[self.source]
