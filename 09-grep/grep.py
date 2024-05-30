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

args = parser.parse_args()

def grep(file_path, regex_pattern, invert):
    # Compile the regular expression pattern
    pattern = re.compile(regex_pattern)
    
    matching_lines = []
    
    # Open the file and read it line by line
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if invert:
                if not pattern.search(line):
                    matching_lines.append(line.rstrip() + '\n')  # Remove trailing whitespace and ensure a single newline
            else:
                if pattern.search(line):
                    matching_lines.append(line.rstrip() + '\n')  # Remove trailing whitespace and ensure a single newline

    # Join the matching lines back into a single string
    result = ''.join(matching_lines)
    
    return result

if __name__ == "__main__":
    file_path = args.filename
    regex_pattern = args.regex
    invert = args.invert

    if args.recursive:
        files = list_files_in_folder(file_path)
        for file in files:
            matched_content = grep(file, regex_pattern, invert)
            print(str(Path.cwd()) + file)
            print(matched_content, end='')  # Print without adding extra newlines
    else:
        matched_content = grep(file_path, regex_pattern, invert)
        print(matched_content, end='')  # Print without adding extra newlines
