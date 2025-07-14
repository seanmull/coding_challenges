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

def get_columns(columns, delimiter, input_stream):
    if not columns:
        print(input_stream)
        return input_stream
    elif "," in columns:
        columns = columns.split(",")
    else:
        columns = columns.split(" ")

    columns = set([int(column) for column in columns])

    table = [line.split(delimiter) for line in input_stream.split("\n")]

    result = []
    # print(table)
    if len(table[-1]) == 0 or table[-1][0] == "":
        table = table[:-1]
    len_table = len(table)
    line_number = 0
    for line in table:
        for i, value in enumerate(line):
            if (i + 1) in columns:
                result.append(f"\t{value}")  
                print(f"\t{value}", end="")
        if line_number < len_table - 1:
            result.append(f"\n")
            print("")
        line_number += 1
    return "".join(result)

if __name__ == "__main__":
    get_columns(columns, delimiter, input_stream)
