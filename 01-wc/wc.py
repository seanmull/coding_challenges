import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Will count the number of bytes, words, lines or characters in file")

parser.add_argument(
    "-c",
    "--bytes",
    action="store_true",
    help="returns the number of bytes in file.",
)

parser.add_argument(
    "-l",
    "--lines",
    action="store_true",
    help="returns the number of lines in a file",
)

parser.add_argument(
    "-w",
    "--words",
    action="store_true",
    help="returns the number of words in a file",
)

parser.add_argument(
    "-m",
    "--characters",
    action="store_true",
    help="returns the number of characters in a file",
)

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

bytes = memoryview(content.encode('utf-8')).nbytes

# TODO this voilates DRY may need to refactor
if args.bytes:
    print('Bytes in file: {} bytes'.format(str(bytes)))
if args.lines:
    print('Lines in file: {} lines'.format(str(content.count("\n"))))
if args.words:
    print('Words in file: {} words'.format(str(len(content.split()))))
if args.characters:
    print('Characters in file: {} characters'.format(str(len(content))))

if not args.bytes and not args.lines and not args.words and not args.characters:
    print('Bytes in file: {} bytes'.format(str(bytes)))
    print('Lines in file: {} lines'.format(str(content.count("\n"))))
    print('Words in file: {} words'.format(str(len(content.split()))))
    print('Characters in file: {} characters'.format(str(len(content))))
