from argparse import ArgumentParser
import ast

from .generator import Generator


def main():
    parser = ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()

    with open(args.file) as file:
        node = ast.parse(file.read(), args.file)

    generator = Generator()
    generator.visit(node)
