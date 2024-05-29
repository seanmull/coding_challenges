import argparse
import re

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(
    description="Will perform grep operations on a file or stdin"
)

parser.add_argument("filename", type=str, nargs="?", help="File you want to readin.")

parser.add_argument("regex", type=str, nargs="?", help="Regular expression")

args = parser.parse_args()

if args.filename:
    file = open(args.filename, "r")
else:
    import sys

    file = sys.stdin

content = file.read()


def find_matching_lines(file_stream, regex_pattern):
    # Compile the regular expression pattern for efficiency
    pattern = re.compile(regex_pattern)

    file_stream = file_stream.split("\n")

    # Read lines from the file stream and filter those that match the pattern
    matching_lines = [line for line in file_stream if pattern.search(line)]

    return "\n".join(matching_lines)

print(find_matching_lines(content, args.regex))
