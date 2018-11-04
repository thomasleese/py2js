"""For emitting JavaScript."""


class Indentation:

    def __init__(self):
        self.level = 0
        self._str = ''

    def __iadd__(self, other):
        self.level += other
        self._reload_str()
        return self

    def __isub__(self, other):
        if self.level < other:
            raise ValueError('Level would end up negative.')
        self.level -= other
        self._reload_str()
        return self

    def _reload_str(self):
        self._str = '  ' * self.level

    def __str__(self):
        return self._str


class Emitter:

    def __init__(self):
        self.indentation = Indentation()
        self.fragments = []

    def __str__(self):
        return ''.join(self.fragments)

    def save(self, filename):
        contents = str(self)

        print(filename)
        print('-' * len(str(filename)))
        print(contents)
        print()

        with open(filename, 'w') as file:
            file.write(contents)

    @property
    def is_new_line(self):
        if not self.fragments:
            return False

        return self.fragments[-1].endswith('\n')

    def emit(self, fragment):
        if self.is_new_line:
            self.fragments.append(str(self.indentation))

        # ignore last character as it could be a new line
        indented = fragment[:-1].replace('\n', '\n' + str(self.indentation))
        fragment = indented + fragment[-1]

        self.fragments.append(fragment)

    def call_or_emit(self, thing):
        if callable(thing):
            thing()
        else:
            self.emit(thing)

    def emit_newline(self):
        self.emit('\n')

    def emit_comma(self, index):
        if index != 0:
            self.emit(', ')

    def emit_semicolon_and_newline(self):
        self.emit(';\n')

    def emit_var(self, name, value):
        self.emit(f'var {name} = ')
        self.call_or_emit(value)
        self.emit_semicolon_and_newline()

    def emit_break(self):
        self.emit('break;\n')

    def emit_return(self, value):
        self.emit(f'return {value};\n')

    def emit_if(self, condition):
        self.emit(f'if ({condition}) {{\n')
        self.indentation += 1

    def emit_else(self):
        self.indentation -= 1
        self.emit('} else {\n')
        self.indentation += 1

    def emit_switch(self, condition):
        self.emit(f'switch ({condition}) {{\n')
        self.indentation += 1

    def deindent_and_emit_closing_brace(self):
        self.indentation -= 1
        self.emit('}\n')

    def emit_opening_brace_and_indent(self, space=True):
        self.emit(f'{" " if space else ""}{{\n')
        self.indentation += 1
