import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Cuts out portions of each line from file")


parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

parser.add_argument(
    "-f",
    "--field",
    type=str, 
    help="Which field we want",
)


args = parser.parse_args()

if args.filename:
    file = open(args.filename, 'r')
else:
    import sys
    file = sys.stdin

content = file.read()

lines = content.split("\n")

table = []
for line in lines:
    tabs = line.split("\t")
    table.append(tabs)
    print(tabs[int(args.field) - 1])


