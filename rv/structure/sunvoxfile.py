from .project import Project


class SunvoxFile(object):

    def __init__(self):
        self.project = Project()
        self.modules = []
