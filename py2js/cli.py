from argparse import ArgumentParser

from .compiler import Compiler


def main():
    parser = ArgumentParser()
    parser.add_argument('file', nargs='+')

    args = parser.parse_args()

    compiler = Compiler()

    for filename in args.file:
        compiler.compile_file(filename)

    print(compiler.emitter)
