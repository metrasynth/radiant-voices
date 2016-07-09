from .project import Project


class SunsynthFile(object):

    def __init__(self):
        self.project = Project()
        self._modules = []

    @property
    def modules(self):
        mlist = self._modules[:]
        while mlist[-1:] == [None]:
            mlist = mlist[:-1]
        return mlist

    def __getstate__(self):
        return dict(
            project=self.project,
            modules=self.modules,
        )
