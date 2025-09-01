import argparse
import re
import sys


parser = argparse.ArgumentParser(
    prog='grep',
    description='Print lines from a file that match a regular expression')
parser.add_argument('pattern')
parser.add_argument('filename', nargs='?')
args = parser.parse_args()

def filter_text(input_file, regex):
    if not input_file or len(input_file) == 0:
        input_steam_stdin = sys.stdin.read()
        input_stream = input_steam_stdin
    else:
        with open(input_file, "r", encoding="utf-8") as file:
            input_stream = file.read()
    lines = input_stream.split("\n")
    # TODO use generators to reduce memory footprint?
    matching = [line for line in lines if re.search(regex, line)]
    print("\n".join(matching))


if __name__ == "__main__":
    filter_text(args.filename, args.pattern)
