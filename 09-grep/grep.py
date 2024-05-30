import re
import sys

def grep(file_path, regex_pattern):
    # Compile the regular expression pattern
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
    # Ensure correct usage
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <file_path> <regex_pattern>")
        sys.exit(1)

    file_path = sys.argv[1]
    regex_pattern = sys.argv[2]

    matched_content = grep(file_path, regex_pattern)
    print(matched_content, end='')  # Print without adding extra newlines

