import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Will parse the json")

parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

args = parser.parse_args()

file = open(args.filename, 'r')

content = file.read()

print("")
