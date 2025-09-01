import argparse
import re
import sys

# TODO add option to recerse the directory tree -r
# TODO add highlighting to matched words
# TODO possibly use generators to deal with matching

parser = argparse.ArgumentParser(
    prog='grep',
    description='Print lines from a file that match a regular expression')
parser.add_argument('pattern')
parser.add_argument('filename', nargs='?')
parser.add_argument('-i', action='store_true')
parser.add_argument('-v', action='store_true')
args = parser.parse_args()


def filter_text(input_file, regex):
    if not input_file or len(input_file) == 0:
        input_steam_stdin = sys.stdin.read()
        input_stream = input_steam_stdin
    else:
        with open(input_file, "r", encoding="utf-8") as file:
            input_stream = file.read()
    lines = input_stream.split("\n")
    if args.v and args.i:
        matching = [line for line in lines if not re.search(
            regex, line, flags=re.IGNORECASE)]
    elif args.i:
        matching = [line for line in lines if re.search(
            regex, line, flags=re.IGNORECASE)]
    elif args.v:
        matching = [line for line in lines if not re.search(regex, line)]
    else:
        matching = [line for line in lines if re.search(regex, line)]
    print("\n".join(matching))


if __name__ == "__main__":
    filter_text(args.filename, args.pattern)
