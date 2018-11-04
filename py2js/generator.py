import ast
from itertools import zip_longest


class Generator(ast.NodeVisitor):

    def __init__(self, emitter):
        self.emitter = emitter
        self.imported_modules = []

    def emit(self, fragment):
        self.emitter.emit(fragment)

    def emit_body(self, body):
        for statement in body:
            self.visit(statement)

    def visit_FunctionDef(self, node):
        self.emit(f'export function {node.name}')
        self.visit(node.args)
        self.emit_body(node.body)
        self.emitter.deindent_and_emit_closing_brace()

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
        self.emit(')')
        self.emitter.emit_opening_brace_and_indent()
        self.emit_body(node.body)
        self.emitter.deindent_and_emit_closing_brace()

    def visit_Import(self, node):
        for name in node.names:
            self.imported_modules.append(name.name)
            asname = name.asname if name.asname else name.name
            self.emit(f'import * as {asname} from "./{name.name}.mjs";\n')

    def visit_Expr(self, node):
        self.visit(node.value)
        self.emit(';\n')

    def visit_ListComp(self, node):
        self.emit('(function ()')
        self.emitter.emit_opening_brace_and_indent()
        self.emitter.emit_var('array', '[]')
        for generator in node.generators:
            self.visit(generator)
        self.emitter.emit_return('array')
        self.emitter.indentation -= 1
        self.emit('}())')

    def visit_Call(self, node):
        self.visit(node.func)
        self.emit('(')

        for i, arg in enumerate(node.args):
            self.emitter.emit_comma(i)
            self.visit(arg)

        if node.keywords:
            self.emitter.emit_comma(len(node.args))
            self.emit('__kwargs__({')
            for i, keyword in enumerate(node.keywords):
                self.emitter.emit_comma(i)
                self.visit(keyword)
            self.emit('})')

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
        # print(node)
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

        self.emitter.emit_opening_brace_and_indent()

        # defaults for keyword arguments
        for arg, expr in zip(node.kwonlyargs, node.kw_defaults):
            if expr:
                self.emitter.emit_var(arg.arg, lambda: self.visit(expr))

        # keyword arguments and varargs
        if node.kwarg:
            self.emitter.emit_var(node.kwarg.arg, '{}')

        self.emitter.emit_if('arguments.length')

        last_arg_index = 'ilastarg'
        all_args = 'allargs'
        attrib_arg = 'attrib'

        self.emitter.emit_var(last_arg_index, 'arguments.length - 1')

        self.emitter.emit_if('arguments[{0}] && arguments[{0}].hasOwnProperty("__kwargs__")'.format(last_arg_index))

        self.emitter.emit_var(all_args, f'arguments[{last_arg_index}--]')
        self.emit(f'for (var {attrib_arg} in {all_args}) {{\n')
        self.emitter.indentation += 1

        self.emitter.emit_switch(attrib_arg)

        for arg in node.args + node.kwonlyargs:
            self.emit(f'case \'{arg.arg}\': ')
            self.emitter.indentation += 1
            self.emitter.emit_var(arg.arg, f'{all_args}[{attrib_arg}]')
            self.emitter.emit_break()
            self.emitter.indentation -= 1

        if node.kwarg:
            self.emit(f'default: {node.kwarg.arg}[{attrib_arg}] = {all_args}[{attrib_arg}];\n')

        self.emitter.deindent_and_emit_closing_brace()
        self.emitter.deindent_and_emit_closing_brace()

        if node.kwarg:
            self.emit(f'delete {node.kwarg.arg}.__kwargs__;\n')

        self.emitter.deindent_and_emit_closing_brace()

        if node.vararg:
            start = len(node.args)
            self.emitter.emit_var(node.vararg.arg, f'[].slice.apply(arguments).slice({start}, {last_arg_index} + 1)')
            self.emitter.emit_else()
            self.emitter.emit_var(node.vararg.arg, '[]')

        self.emitter.deindent_and_emit_closing_brace()

    def visit_arg(self, node):
        self.emit(node.arg)

    def visit_keyword(self, node):
        self.emit(node.arg)
        self.emit(': ')
        self.visit(node.value)
