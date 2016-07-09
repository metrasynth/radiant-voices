class Pattern(object):

    def __init__(self):
        self.property_flags = 0
        self.selection_flags = 0

    @property
    def is_selected(self):
        return bool(self.selection_flags & 2)

    @property
    def has_no_icon(self):
        return bool(self.property_flags & 1)
