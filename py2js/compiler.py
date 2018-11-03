import ast
from pathlib import Path
import pkg_resources

from .emitter import Emitter
from .generator import Generator


class Compiler:

    def __init__(self, output_dir):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.compile_runtime()

    def compile_source(self, emitter, source, filename):
        node = ast.parse(source, filename)
        generator = Generator(emitter)
        generator.visit(node)

    def read_builtins(self):
        filename = 'runtime/__builtins__.js'
        return pkg_resources.resource_string(__name__, filename).decode()

    def compile_runtime(self):
        emitter = Emitter()
        emitter.emit(self.read_builtins())
        emitter.emit_newline()

        filename = 'runtime/__builtins__.py'
        source = pkg_resources.resource_string(__name__, filename)
        self.compile_source(emitter, source, '__builtins__.py')

        emitter.save(self.output_dir / '__builtins__.mjs')

    def compile_file(self, filename):
        with open(filename) as file:
            source = file.read()

        emitter = Emitter()
        emitter.emit('import {__kwargs__, print} from "./__builtins__.mjs";\n')

        self.compile_source(emitter, source, filename)

        output_filename = Path(filename).name.replace('.py', '.mjs')

        js_path = self.output_dir / output_filename
        emitter.save(js_path)
        return js_path
