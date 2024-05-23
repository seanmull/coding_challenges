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

args = parser.parse_args()

if args.filename:
    file = open(args.filename, 'r')
else:
    import sys
    file = sys.stdin

content = file.read()

words = content.split("\n")

words.sort()

for word in words:
    if len(word) > 0:
        print(word)

