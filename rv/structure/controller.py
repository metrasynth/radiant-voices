class _Definition(object):

    def __init__(self, *args):
        pass


class Controller(object):

    def __init__(self, index, name, min, max, range):
        self.index = index
        self.name = name
        self.min = min
        self.max = max
        self.range = range


class Choices(object):

    def __init__(self, *choices):
        self.choices = choices


class OnOff(Choices):

    def __init__(self):
        super().__init__(False, True)


class Range(object):

    def __init__(self, min, max):
        self.min = min
        self.max = max
