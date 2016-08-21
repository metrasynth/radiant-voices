"""
"Hello World"

This shows the construction of a SunVox project using Radiant Voices,
then loading that projet into sunvox-dll-python and playing a note.
"""

from rv import ENCODING
from rv.modules import Fm
from rv.project import Project
import sunvox


def hello_world():
    print('Building project')
    project = Project()
    fm_synth = project.new_module(Fm, m_feedback=42)
    project.connect(fm_synth, project.output)

    print('Writing project to output.sunvox')
    with open('output.sunvox', 'wb') as f:
        project.write_to(f)

    print('Initializing SunVox DLL')
    sunvox.init(None, 44100, 2, 0)

    print('Opening slot and reading buffer')
    with sunvox.Slot(project) as slot:
        for i in range(slot.get_number_of_modules()):
            name = slot.get_module_name(i).decode(ENCODING)
            print('Module {}: {}'.format(i, name))
        print('Sending event to slot {}'.format(slot.number))
        slot.send_event(0, 42, 32, fm_synth, 0, 0)
        print('Press Enter to close')
        input()

    print('Deinitializing SunVox DLL')
    sunvox.deinit()


if __name__ == '__main__':
    hello_world()
