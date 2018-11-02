from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('file')

    args = parser.parse_args()
    print(args)
