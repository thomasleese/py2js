"""For emitting JavaScript."""


class Emitter:

    def __init__(self):
        self.fragments = []
        self.indent_level = 0

    def __str__(self):
        return ''.join(self.fragments)

    @property
    def is_new_line(self):
        if not self.fragments:
            return False

        return self.fragments[-1].endswith('\n')

    @property
    def indentation(self):
        return '  ' * self.indent_level

    def indent(self):
        self.indent_level += 1

    def deindent(self):
        self.indent_level -= 1

    def emit(self, fragment):
        if self.is_new_line:
            self.fragments.append(self.indentation)

        # ignore last character as it could be a new line
        indented = fragment[:-1].replace('\n', '\n' + self.indentation)
        fragment = indented + fragment[-1]

        self.fragments.append(fragment)

    def emit_comma(self, index):
        if index != 0:
            self.emit(', ')
