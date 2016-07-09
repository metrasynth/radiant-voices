class _Definition(object):

    def __init__(self, *args):
        pass


class Controller(object):

    def __init__(self, index, value_type):
        self.index = index
        self.value_type = value_type


class Range(object):

    def __init__(self, min, max):
        self.min = min
        self.max = max

    def __call__(self, raw_value):
        return raw_value + self.min if self.min < 0 else raw_value
