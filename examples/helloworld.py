"""
"Hello World"

This shows the construction of a SunVox project using Radiant Voices,
then loading that project into sunvox-dll-python and playing a note.
"""

from rv.modules import Fm
from rv.project import Project
import sunvox


def hello_world():
    project = Project()
    fm = project.new_module(Fm, m_feedback=42)
    project.connect(fm, project.output)
    sunvox.init(None, 44100, 2, 0)
    with sunvox.Slot(project) as slot:
        slot.send_event(0, 42, 32, fm, 0, 0)
        print('Press Enter to close')
        input()
        slot.stop()
    sunvox.deinit()


if __name__ == '__main__':
    hello_world()
