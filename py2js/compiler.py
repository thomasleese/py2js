import ast
import pkg_resources

from .emitter import Emitter
from .generator import Generator


class Compiler:

    def compile_source(self, source, filename='unknown'):
        node = ast.parse(source, filename)

        emitter = Emitter()
        generator = Generator(emitter)
        generator.visit(node)

        return str(emitter)

    def load_builtins(self):
        filename = 'runtime/__builtins__.js'
        return pkg_resources.resource_string(__name__, filename).decode()

    def compile_runtime(self):
        filename = 'runtime/__builtins__.py'
        source = pkg_resources.resource_string(__name__, filename)
        return self.compile_source(source, '__builtins__.py')

    def compile(self, filename):
        builtins = self.load_builtins()
        runtime_compiled = self.compile_runtime()

        with open(filename) as file:
            source = file.read()

        compiled = self.compile_source(source, filename)
        return builtins + '\n' + runtime_compiled + '\n' + compiled
