import ast

from .emitter import Emitter
from .generator import Generator


def compile_source(source, filename='unknown'):
    node = ast.parse(source, filename)

    emitter = Emitter()
    generator = Generator(emitter)
    generator.visit(node)

    return str(emitter)


def compile(filename):
    with open(filename) as file:
        source = file.read()
    print(compile_source(source, filename))
