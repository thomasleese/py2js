import ast
import pkg_resources

from .emitter import Emitter
from .generator import Generator


class Compiler:

    def __init__(self):
        self.emitter = Emitter()
        self.load_runtime()

    def compile_source(self, source, filename='unknown'):
        node = ast.parse(source, filename)
        generator = Generator(self.emitter)
        generator.visit(node)

    def load_runtime(self):
        self.emitter.emit(self.read_builtins())
        self.compile_runtime()

    def read_builtins(self):
        filename = 'runtime/__builtins__.js'
        return pkg_resources.resource_string(__name__, filename).decode()

    def compile_runtime(self):
        filename = 'runtime/__builtins__.py'
        source = pkg_resources.resource_string(__name__, filename)
        self.compile_source(source, '__builtins__.py')

    def compile_file(self, filename):
        with open(filename) as file:
            source = file.read()
        self.compile_source(source, filename)

    def compile(self, filename):
        self.compile_file(filename)
        return str(self.emitter)
