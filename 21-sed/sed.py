import argparse
import re
import sys
import shutil

def apply_regex_substitution(regex_str, target_str):
    # Extract the pattern and the replacement from the regex_str
    # The regex_str format is expected to be "s/<pattern>/<replacement>/g"
    match = re.match(r's/(.*)/(.*)/g', regex_str)
    if match:
        pattern = match.group(1)
        replacement = match.group(2)
        
        # Apply the substitution
        result = re.sub(pattern, replacement, target_str)
        return result
    else:
        raise ValueError("Invalid regex substitution string format")

def print_lines_matching_pattern(pattern, target_str, double_space=False):
    lines = target_str.split("\n")
    matched_lines = [line for line in lines if re.search(pattern, line)]
    output = "\n".join(matched_lines)
    if double_space:
        output = "\n\n".join(output.split("\n"))
    return output.strip("\n")  # Strip trailing newlines

def main(args):
    inplace = False
    if args.inplace:
        inplace = True

    full_content = ""
    if args.filename and args.filename[0] != sys.stdin:
        for filename in args.filename:
            with open(filename, "r") as file:
                content = file.read()
                full_content += content
                if inplace:
                    shutil.copy(filename, filename + '.bak')
    else:
        full_content = sys.stdin.read()
    
    if args.range:
        args.range = args.range.replace("p", "")
        parts = args.range.split(",")
        if len(parts) == 1:
            full_content = full_content.split("\n")
            full_content = full_content[int(parts[0]) - 1]
        elif len(parts) == 2:
            full_content = full_content.split("\n")
            full_content = full_content[int(parts[0]) - 1: int(parts[1]) - 1]
            full_content = "\n".join(full_content)
        else:
            print("error")

    if args.regex.startswith("/") and (args.regex.endswith("/p") or args.regex.endswith("/d")):
        # Remove leading and trailing slashes and '/p'
        pattern = args.regex[1:-2]
        matched_lines = print_lines_matching_pattern(pattern, full_content, args.double_space)
        if inplace:
            with open(args.filename[0], "w") as file:
                file.write(matched_lines)
        else:
            print(matched_lines, end="")
    else:
        replaced = apply_regex_substitution(args.regex, full_content)
        if inplace:
            with open(args.filename[0], "w") as file:
                file.write(replaced)
        else:
            print(replaced[:-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write to stdout from file or stdin")
    parser.add_argument("regex", type=str, help="Regular expression or pattern to apply to data stream")
    parser.add_argument("filename", nargs="*", default=[sys.stdin], help="Files want to write to stdout (default: stdin)")
    parser.add_argument(
        "-n",
        "--range",
        type=str,
        help="returns the number of characters in a file",
    )
    parser.add_argument(
        "-G",
        "--double-space",
        action="store_true",
        help="Double space the output",
    )
    parser.add_argument(
        "-i",
        "--inplace",
        action="store_true",
        help="Edit files in place",
    )

    args = parser.parse_args()

    main(args)

