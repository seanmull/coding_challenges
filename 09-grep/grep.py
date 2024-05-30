import re
from pathlib import Path
import argparse
from utils import list_files_in_folder

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Replicates the functionality of grep")

parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

parser.add_argument(
        "regex", 
        type=str, 
        nargs="?", 
        help="Regular expression")

parser.add_argument(
    "-r",
    "--recursive",
    action="store_true",
    help="Recursively call files within a folder",
)

parser.add_argument(
    "-v",
    "--invert",
    action="store_true",
    help="Inverts the find",
)

parser.add_argument(
    "-i",
    "--insensitive",
    action="store_true",
    help="Case insensitive search",
)

args = parser.parse_args()

def grep(file_path, regex_pattern, invert, insensitive):
    # Compile the regular expression pattern
    if insensitive and invert:
        regex_pattern = rf'(?:(?!{regex_pattern}).)*$'
        pattern = re.compile(regex_pattern, re.IGNORECASE)
    elif insensitive and not invert:
        pattern = re.compile(regex_pattern, re.IGNORECASE)
    elif not insensitive and invert:
        regex_pattern = rf'(?:(?!{regex_pattern}).)*$'
        pattern = re.compile(regex_pattern)
    else:
        pattern = re.compile(regex_pattern)
    
    matching_lines = []
    
    # Open the file and read it line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if pattern.search(line):
                matching_lines.append(line.rstrip() + '\n')  # Remove trailing whitespace and ensure a single newline

    # Join the matching lines back into a single string
    result = ''.join(matching_lines)
    
    return result

if __name__ == "__main__":
    file_path = args.filename
    regex_pattern = args.regex
    invert = args.invert
    insensitive = args.insensitive

    if args.recursive:
        files = list_files_in_folder(file_path)
        for file in files:
            matched_content = grep(file, regex_pattern, invert, insensitive)
            print(str(Path.cwd()) + file)
            print(matched_content, end='')  # Print without adding extra newlines
    else:
        matched_content = grep(file_path, regex_pattern, invert, insensitive)
        print(matched_content, end='')  # Print without adding extra newlines
