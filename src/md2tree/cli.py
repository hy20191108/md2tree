import argparse

from md2tree import md2tree


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Convert markdown to tree structure")
    parser.add_argument("input", help="Input markdown file")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    md2tree.convert(args.input)
