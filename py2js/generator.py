import ast
from collections import defaultdict
from itertools import zip_longest


class TemporaryVariable:

    def __init__(self, name):
        self.name = name
        self.index = 0

    def __str__(self):
        return f'__{self.name}{self.index}__'

    def __enter__(self):
        self.index += 1
        return str(self)

    def __exit__(self, *args):
        self.index -= 1
        return False


class TemporaryVariables(defaultdict):

    def __missing__(self, key):
        self[key] = var = TemporaryVariable(key)
        return var


class ScopeContext:

    def __init__(self, scope, node):
        self.scope = scope
        self.node = node

    def __enter__(self):
        self.scope.push(self.node)

    def __exit__(self, *args):
        self.scope.pop()
        return False


class Scope:

    def __init__(self):
        self.nodes = []

    def __call__(self, node):
        return ScopeContext(self, node)

    def push(self, node):
        self.nodes.append(node)

    def pop(self):
        self.nodes.pop()

    @property
    def node(self):
        return self.nodes[-1]

    @property
    def in_module(self):
        return isinstance(self.node, ast.Module)

    @property
    def in_class(self):
        return isinstance(self.node, ast.ClassDef)


class Generator(ast.NodeVisitor):

    def __init__(self, emitter):
        self.emitter = emitter
        self.temp_vars = TemporaryVariables()
        self.scope = Scope()
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

        with self.temp_vars['ilastarg'] as arguments_last_index_var, self.temp_vars['kwargs'] as kwargs_var, self.temp_vars['kwarg'] as kwarg_var:
            self.emitter.emit_var(arguments_last_index_var, 'arguments.length - 1')

            self.emitter.emit_if(
                'arguments[{0}] && arguments[{0}].hasOwnProperty("__kwargs__")'.format(arguments_last_index_var)
            )

            self.emitter.emit_var(kwargs_var, f'arguments[{arguments_last_index_var}--]')
            self.emit(f'for (var {kwarg_var} in {kwargs_var}) {{\n')
            self.emitter.indentation += 1

            self.emitter.emit_switch(kwarg_var)

            for arg in node.args + node.kwonlyargs:
                self.emit(f'case \'{arg.arg}\': ')
                self.emitter.indentation += 1
                self.emitter.emit_var(arg.arg, f'{kwargs_var}[{kwarg_var}]')
                self.emitter.emit_break()
                self.emitter.indentation -= 1

            if node.kwarg:
                self.emit(f'default: {node.kwarg.arg}[{kwarg_var}] = {kwargs_var}[{kwarg_var}];\n')

            self.emitter.deindent_and_emit_closing_brace()
            self.emitter.deindent_and_emit_closing_brace()

            if node.kwarg:
                self.emit(f'delete {node.kwarg.arg}.__kwargs__;\n')

            self.emitter.deindent_and_emit_closing_brace()

            if node.vararg:
                start = len(node.args)
                self.emitter.emit_var(
                    node.vararg.arg, f'[].slice.apply(arguments).slice({start}, {arguments_last_index_var} + 1)'
                )
                self.emitter.emit_else()
                self.emitter.emit_var(node.vararg.arg, '[]')

            self.emitter.deindent_and_emit_closing_brace()

    def visit_arg(self, node):
        self.emit(node.arg)

    def visit_keyword(self, node):
        self.emit(node.arg)
        self.emit(': ')
        self.visit(node.value)
