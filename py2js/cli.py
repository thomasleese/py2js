from argparse import ArgumentParser

from .compiler import compile


def main():
    parser = ArgumentParser()
    parser.add_argument('file', nargs='+')

    args = parser.parse_args()

    for filename in args.file:
        compile(filename)
