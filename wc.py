import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Will count the number of bytes, words, lines or characters in file")

parser.add_argument(
    "-c",
    "--bytes",
    action="store_true",
    help="Will be either True or False",
)

parser.add_argument("filename", type=str, help="File you want to readin.")

args = parser.parse_args()

file = open(args.filename, 'r')

content = file.read()

bytes = memoryview(content.encode('utf-8')).nbytes

print('Bytes in file: {} bytes'.format(str(bytes)))
