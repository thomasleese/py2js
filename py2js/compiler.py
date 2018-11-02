import ast

from .emitter import Emitter
from .generator import Generator


def compile(filename):
    with open(filename) as file:
        node = ast.parse(file.read(), filename)

    emitter = Emitter()
    generator = Generator(emitter)
    generator.visit(node)

    print(emitter)
