import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Will return the a result with only unique lines.")


parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

parser.add_argument(
    "-c",
    "--count",
    action="store_true",
    help="provides a column that shows how many repeats of each line",
)

parser.add_argument(
    "-d",
    "--repeated",
    action="store_true",
    help="Only shows the repeated lines.",
)

parser.add_argument(
    "-u",
    "--unique",
    action="store_true",
    help="Only shows the repeated lines.",
)

args = parser.parse_args()

if args.filename:
    file = open(args.filename, 'r')
else:
    import sys
    file = sys.stdin

content = file.read()

lines = content.split("\n")

cache = {}

for line in lines:
    if len(line) == 0:
        continue
    if line not in cache:
        cache[line] = 1
    else:
        cache[line] += 1

start = 0
end = len(cache.items())

for key, value in cache.items():
    if start >= end:
        break
    if args.repeated:
        if args.count and (value > 1):
            print (f"{value}\t{key}")
        elif value > 1:
            print (f"{key}")
    elif args.unique:
        if args.count and (value == 1):
            print (f"{value}\t{key}")
        elif value == 1:
            print (f"{key}")
    else:
        if args.count:
            print (f"{value}\t{key}")
        else:
            print (f"{key}")
    start += 1
