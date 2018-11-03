"""For emitting JavaScript."""


class Emitter:

    def __init__(self):
        self.fragments = []
        self.indent_level = 0

    def __str__(self):
        return ''.join(self.fragments)

    def save(self, filename):
        with open(filename, 'w') as file:
            file.write(str(self))

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

    def emit_newline(self):
        self.emit('\n')

    def emit_comma(self, index):
        if index != 0:
            self.emit(', ')

    def emit_else(self):
        self.deindent()
        self.emit('} else {\n')
        self.indent()

    def deindent_and_emit_closing_brace(self):
        self.deindent()
        self.emit('}\n')
