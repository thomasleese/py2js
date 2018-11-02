import ast


class Generator(ast.NodeVisitor):

    def __init__(self, emitter):
        self.emitter = emitter

    def emit(self, fragment):
        self.emitter.emit(fragment)

    def visit_Assign(self, node):
        self.emit('var ')

        for i, target in enumerate(node.targets):
            if i != 0:
                self.emit(', ')
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
