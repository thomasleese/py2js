import ast

from .emitter import Emitter
from .generator import Generator


def compile_source(source, filename='unknown'):
    node = ast.parse(source, filename)

    emitter = Emitter()
    generator = Generator(emitter)
    generator.visit(node)

    return str(emitter)


def load_builtins():
    with open('runtime/__builtins__.js') as file:
        return file.read()


def compile_runtime():
    with open('runtime/core.py') as file:
        source = file.read()
    return compile_source(source, 'runtime/core.py')


def compile(filename):
    builtins = load_builtins()
    runtime_compiled = compile_runtime()

    with open(filename) as file:
        source = file.read()
    compiled = compile_source(source, filename)
    return builtins + '\n' + runtime_compiled + '\n' + compiled
