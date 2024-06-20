import argparse
import re
import sys

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

def main(args):
    full_content = ""
    if args.filename:
        for filename in args.filename:
            with open(filename, "r") as file:
                content = file.read()
                full_content += content
    else:
        full_content = sys.stdin.read()
    
    replaced = apply_regex_substitution(args.regex, full_content)
    print(replaced[:-1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write to stdout from file or stdin")
    parser.add_argument("regex", type=str, help="Regular expression you want to apply to data stream")
    parser.add_argument("filename", nargs="*", help="Files want to write to stdout")
    args = parser.parse_args()

    main(args)

