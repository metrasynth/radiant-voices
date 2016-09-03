# Cyrillic script; see https://en.wikipedia.org/wiki/Windows-1251
ENCODING = 'cp1251'

import rv.modules
from rv.note import Note, NOTE, NOTECMD
from rv.pattern import Pattern, PatternClone
from rv.project import Project
from rv.readers.reader import read_sunvox_file
from rv.synth import Synth
