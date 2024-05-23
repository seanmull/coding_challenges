import argparse
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL) 
# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Sorts through words.")

parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

parser.add_argument(
    "-u",
    "--unique",
    action="store_true",
    help="flag for unique char",
)

args = parser.parse_args()

if args.filename:
    file = open(args.filename, 'r')
else:
    import sys
    file = sys.stdin

content = file.read()

words = content.split("\n")

if args.unique:
    words = list(set(words))

words.sort()

for word in words:
    if len(word) > 0:
        print(word)

