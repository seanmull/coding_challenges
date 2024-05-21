import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Cuts out portions of each line from file")


parser.add_argument("filename", type=str, nargs="?", help="File you want to readin.")

parser.add_argument(
    "-f",
    "--field",
    default="0",
    help="Which field we want",
)

parser.add_argument(
    "-d",
    "--delimiter",
    type=str,
    nargs="?",
    help="What delimiter you need",
)

args = parser.parse_args()

if not args.delimiter:
    args.delimiter = "\t"

if args.filename:
    file = open(args.filename, "r")
else:
    import sys

    file = sys.stdin

content = file.read()

if "," in args.field:
    args.field = args.field.split(",")
elif "\t" in args.field:
    args.field = args.field.split("\t")

lines = content.split("\n")

table = []
for line in lines:
    tabs = line.split(args.delimiter)
    table.append(tabs)
    for i, field in enumerate(args.field):
        if i == len(args.field) - 1:
            print(tabs[int(field) - 1], end="")
        else:
            print(tabs[int(field) - 1] + args.delimiter, end="")
    print()
