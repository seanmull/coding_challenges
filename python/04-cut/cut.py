#!/usr/bin/env python
import argparse
import sys

parser = argparse.ArgumentParser(
                    prog='cut',
                    description='Provides columns of a csv, or tsv table')
parser.add_argument('filename', nargs='?')
parser.add_argument('-f', '--fields')
parser.add_argument('-d', '--delimiter')
args = parser.parse_args()

# default to read stdin if there
if not args.filename or  len(args.filename) == 0:
    input_steam_stdin = sys.stdin.read()
    input_stream = input_steam_stdin
else:
    # ensure the file closes by using "with"
    with open(args.filename, "r", encoding="utf-8") as file:
        input_stream = file.read()

columns = args.fields
if not args.delimiter:
    delimiter = "\t"
else:
    delimiter = args.delimiter



if not columns:
    print(input_stream)
    exit(1)
elif "," in columns:
    columns = columns.split(",")
else:
    columns = columns.split(" ")

columns = set([int(column) for column in columns])

table = [line.split(delimiter) for line in input_stream.split("\n")]

for line in table:
    for i, value in enumerate(line):
        if (i + 1) in columns:
            print(f"\t{value}", end="")
    print("")
