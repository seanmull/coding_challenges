import argparse
from utils import lcs, generate_diff

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Will provide a diff of two files")


parser.add_argument(
        "filename1", 
        type=str, 
        nargs="?", 
        help="One file you want to compare")

parser.add_argument(
        "filename2", 
        type=str, 
        nargs="?", 
        help="Another file you want to compare")

args = parser.parse_args()

file1 = open(args.filename1, 'r')
file2 = open(args.filename2, 'r')

content1 = file1.read()
content2 = file2.read()

content1 = content1.split("\n")
content2 = content2.split("\n")

common_lines = lcs(content1, content2)
print(generate_diff(content1, content2, common_lines))


