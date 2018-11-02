from argparse import ArgumentParser

from .compiler import compile


def main():
    parser = ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()

    compile(args.file)
