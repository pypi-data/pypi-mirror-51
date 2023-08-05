from .baseclass import DocumentBaseClass


class TextClass(DocumentBaseClass):
    def __init__(self, text, include_extra_newline_after=False):
        self.text = text
        self.include_extra_newline_after = include_extra_newline_after

    def __repr__(self):
        repr = self.text
        if self.include_extra_newline_after:
            repr += "\n"
        return repr
