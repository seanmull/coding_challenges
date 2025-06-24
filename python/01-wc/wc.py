import string
import sys
import argparse

parser = argparse.ArgumentParser(
                    prog='wc',
                    description='Counts the number of lines, words, characters, bytes from a file stream')
parser.add_argument('filename')
parser.add_argument('-l', '--lines')
parser.add_argument('-w', '--words')
parser.add_argument('-c', '--chars')
parser.add_argument('-m', '--bytes')
args = parser.parse_args()

# default to read stdin if there
if len(args.filename) == 0:
    input_steam_stdin = sys.stdin.read()
    input_stream = input_steam_stdin
else:
    # ensure the file closes by using "with"
    with open(args.filename, "r", encoding="utf-8") as file:
        input_stream = file.read()

number_of_char = len(input_stream)

number_of_words = 0
word_has_ended = True
number_of_lines = 0

for character in input_stream:
    if character == "\n":
        number_of_lines += 1
    if character not in string.whitespace and word_has_ended:
        number_of_words += 1
        word_has_ended = False
    elif character in string.whitespace:
        word_has_ended = True

# if end with a newline we don't assume a break afterwards
if input_stream[-1] != "\n":
    number_of_lines += 1

print_all = (not args.lines) and \
            (not args.words) and \
            (not args.chars) and \
            (not args.bytes)

number_of_bytes = len(input_stream.encode("utf-8"))
if print_all:
    print(f'{number_of_lines} {number_of_words} {number_of_bytes}')
elif args.lines:
    print(f'{number_of_lines}')
elif args.words:
    print(f'{number_of_words}')
elif args.bytes:
    print(f'{number_of_bytes}')
elif args.chars:
    print(f'{number_of_char}')
