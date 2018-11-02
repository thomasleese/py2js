import ast


class Generator(ast.NodeVisitor):

    def __init__(self, emitter):
        self.emitter = emitter

    def emit(self, fragment):
        self.emitter.emit(fragment)

    def visit_FunctionDef(self, node):
        self.emit('function ')
        self.emit(node.name)
        self.visit(node.args)
        for statement in node.body:
            self.visit(statement)
        self.emitter.deindent()
        self.emit('}\n')

    def visit_Assign(self, node):
        self.emit('var ')

        for i, target in enumerate(node.targets):
            self.emitter.emit_comma(i)
            self.visit(target)

        self.emit(' = ')
        self.visit(node.value)
        self.emit(';\n')

    def visit_Expr(self, node):
        self.visit(node.value)
        self.emit(';\n')

    def visit_Call(self, node):
        self.visit(node.func)
        self.emit('(')
        for arg in node.args:
            self.visit(arg)
        self.emit(')')

    def visit_Str(self, node):
        self.emit('"')
        self.emit(node.s)
        self.emit('"')

    def visit_Name(self, node):
        self.emit(node.id)

    def visit_Attribute(self, node):
        self.visit(node.value)
        self.emit('.')
        self.emit(node.attr)

    def visit_arguments(self, node):
        self.emit('(')
        for i, arg in enumerate(node.args):
            self.emitter.emit_comma(i)
            self.visit(arg)
        self.emit(')')

        self.emit(' {\n')
        self.emitter.indent()

        for arg, expr in reversed(list(zip(reversed(node.args), reversed(node.defaults)))):
            if expr is None:
                continue

            self.emit(f'if (typeof {arg.arg} == "undefined")')
            self.emit(' {\n')
            self.emitter.indent()
            self.emit(f'var {arg.arg} = ')
            self.visit(expr)
            self.emit(';\n')
            self.emitter.deindent()
            self.emit('}\n')

    def visit_arg(self, node):
        self.emit(node.arg)
