from .project import Project


class SunvoxFile(object):

    def __init__(self):
        self.project = Project()
        self._modules = []
        self._patterns = []

    @property
    def modules(self):
        L = self._modules[:]
        while L[-1] is None:
            L = L[:-1]
        return L

    @property
    def patterns(self):
        L = self._patterns[:]
        while L[-1] is None:
            L = L[:-1]
        return L
