import ast
from itertools import zip_longest


class Generator(ast.NodeVisitor):

    def __init__(self, emitter):
        self.emitter = emitter

    def emit(self, fragment):
        self.emitter.emit(fragment)

    def emit_body(self, body):
        for statement in body:
            self.visit(statement)

    def visit_FunctionDef(self, node):
        self.emit('function ')
        self.emit(node.name)
        self.visit(node.args)
        self.emit_body(node.body)
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

    def visit_For(self, node):
        self.emit('for (var ')
        self.visit(node.target)
        self.emit(' of ')
        self.visit(node.iter)
        self.emit(') {\n')
        self.emitter.indent()
        self.emit_body(node.body)
        self.emitter.deindent()
        self.emit('}\n')

    def visit_Expr(self, node):
        self.visit(node.value)
        self.emit(';\n')

    def visit_ListComp(self, node):
        self.emit('(function () {\n')
        self.emitter.indent()
        self.emit('var array = [];\n')
        for generator in node.generators:
            self.visit(generator)
        self.emit('return array;\n')
        self.emitter.deindent()
        self.emit('}())')

    def visit_Call(self, node):
        self.visit(node.func)
        self.emit('(')

        for i, arg in enumerate(node.args):
            self.emitter.emit_comma(i)
            self.visit(arg)

        self.emitter.emit_comma(len(node.args))
        self.emit('{')
        for i, keyword in enumerate(node.keywords):
            self.emitter.emit_comma(i)
            self.visit(keyword)
        self.emit('}')

        self.emit(')')

    def visit_Str(self, node):
        string = node.s.replace('\n', '\\n')
        self.emit(f"'{string}'")

    def visit_Name(self, node):
        self.emit(node.id)

    def visit_Attribute(self, node):
        self.visit(node.value)
        self.emit('.')
        self.emit(node.attr)

    def visit_List(self, node):
        self.emit('[')
        for i, element in enumerate(node.elts):
            self.emitter.emit_comma(i)
            self.visit(element)
        self.emit(']')

    def visit_comprehension(self, node):
        #print(node)
        pass

    def visit_arguments(self, node):
        self.emit('(')

        # positional arguments
        args_with_default = reversed(
            list(zip_longest(reversed(node.args), reversed(node.defaults)))
        )

        for i, (arg, default_expr) in enumerate(args_with_default):
            self.emitter.emit_comma(i)
            self.visit(arg)

            if default_expr:
                self.emit(' = ')
                self.visit(default_expr)

        self.emit(')')

        self.emit(' {\n')
        self.emitter.indent()

        # defaults for keyword arguments
        for arg, expr in zip(node.kwonlyargs, node.kw_defaults):
            if expr:
                self.emit(f'var {arg.arg} = ')
                self.visit(expr)
                self.emit(';\n')

        # keyword arguments and varargs
        if node.kwarg:
            self.emit(f'var {node.kwarg.arg} = {{}};\n')

        self.emit('if (arguments.length) {\n')
        self.emitter.indent()

        last_arg_index = 'ilastarg'
        all_args = 'allargs'
        attrib_arg = 'attrib'

        self.emit(f'var {last_arg_index} = arguments.length - 1;\n')
        self.emit(f'var {all_args} = arguments[{last_arg_index}];\n')
        self.emit(f'for (var {attrib_arg} in {all_args}) {{\n')
        self.emitter.indent()

        self.emit(f'switch ({attrib_arg}) {{\n')
        self.emitter.indent()

        for arg in node.args + node.kwonlyargs:
            self.emit(f'case \'{arg.arg}\': var {arg.arg} = {all_args}[{attrib_arg}]; break;\n')

        if node.kwarg:
            self.emit(f'default: {node.kwarg.arg}[{attrib_arg}] = {all_args}[{attrib_arg}];\n')

        self.emitter.deindent_and_emit_closing_brace()

        self.emitter.deindent_and_emit_closing_brace()

        if node.vararg:
            start = len(node.args)
            self.emit(f'var {node.vararg.arg} = [].slice.apply(arguments).slice({start}, {last_arg_index});\n')
            self.emitter.emit_else()
            self.emit(f'var {node.vararg.arg} = [];\n')

        self.emitter.deindent()
        self.emit('}\n')

    def visit_arg(self, node):
        self.emit(node.arg)

    def visit_keyword(self, node):
        self.emit(node.arg)
        self.emit(': ')
        self.visit(node.value)
