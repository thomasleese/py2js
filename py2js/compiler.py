import ast
import pkg_resources

from .emitter import Emitter
from .generator import Generator


def compile_source(source, filename='unknown'):
    node = ast.parse(source, filename)

    emitter = Emitter()
    generator = Generator(emitter)
    generator.visit(node)

    return str(emitter)


def load_builtins():
    filename = 'runtime/__builtins__.js'
    return pkg_resources.resource_string(__name__, filename).decode()


def compile_runtime():
    filename = 'runtime/__builtins__.py'
    source = pkg_resources.resource_string(__name__, filename)
    return compile_source(source, '__builtins__.py')


def compile(filename):
    builtins = load_builtins()
    runtime_compiled = compile_runtime()

    with open(filename) as file:
        source = file.read()

    compiled = compile_source(source, filename)
    return builtins + '\n' + runtime_compiled + '\n' + compiled
