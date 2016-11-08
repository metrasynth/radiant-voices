from rv import ENCODING
import rv.modules
from rv.note import Note, NOTE, NOTECMD
from rv.pattern import Pattern, PatternClone
from rv.project import Project
from rv.readers.reader import read_sunvox_file
from rv.synth import Synth

m = rv.modules

rv.m = rv.modules
rv.Note = Note
rv.NOTE = NOTE
rv.NOTECMD = NOTECMD
rv.Pattern = Pattern
rv.PatternClone = PatternClone
rv.Project = Project
rv.read_sunvox_file = read_sunvox_file
rv.Synth = Synth
