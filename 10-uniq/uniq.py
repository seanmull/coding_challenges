import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Will return the a result with only unique lines.")


parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

args = parser.parse_args()

if args.filename:
    file = open(args.filename, 'r')
else:
    import sys
    file = sys.stdin

content = file.read()

lines = content.split("\n")

cache = set()

for line in lines:
    if line not in cache:
        print(line)
    cache.add(line)
