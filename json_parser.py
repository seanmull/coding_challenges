import argparse
import re
import pprint

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

# TODO need to figure out a way to allow the comma to be missing in the end only
regex = '{(\s*"[\w-]*"\s*:{1}\s*("\w*"|\[\s*\]|true|false|null|\{\s*\}|\d*)\s*,\n*)*}'

match = re.match(regex, content)

if match:
    print("The json file is valid.")
else:
    print("The json file is invalid.")
    exit()

obj = {}

stripedcontent = content.strip().strip("{}")

stripedcontentarr = stripedcontent.split(",")

if len(stripedcontentarr) == 1 and stripedcontentarr[0] == "":
    print("{}")
else:
    for ele in stripedcontentarr:
        if ele == "\n":
            continue
        key, value = ele.split(":")
        key = key.strip()
        value = value.strip()
        if value == "null":
            value = None
        elif value == "true":
            value = True
        # need to capture possiblity that whitespace is between brackets
        elif value == "[]":
            value = []
        elif value == "{}":
            value = {}
        elif value == "false":
            value = False
        else:
            try:
                value = int(value)
            except ValueError:
                print(value + " is not a number.")
        obj[key] = value

pprint.pp(obj)
