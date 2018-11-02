import ast


class Parser(ast.NodeVisitor):

    def generic_visit(self, node):
        print(node)
        super().generic_visit(node)
