import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for


def main(args):
    full_content = ""
    if args.arguments:
        for arg in args.arguments:
            file = open(arg, "r")
            content = file.read()
            content = content[:-1]
            full_content += content
    else:
        import sys
        file = sys.stdin

    if args.numberoflines:
        for i, line in enumerate(full_content.split("\n")):
            print(f"{i} {line}")
    elif args.numberoflinewiththenewline:
        counter = 0
        for line in full_content.split("\n"):
            if len(line) != 0:
                print(f"{counter} {line}")
                counter += 1
            else:
                print("")
    else:
        print(full_content)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Write to stdout from file or stdin")

    parser.add_argument("arguments", nargs="*", help="Files want to write to stdout")
    
    parser.add_argument(
        "-n",
        "--numberoflines",
        action="store_true",
        help="Print number lines",
    )

    parser.add_argument(
        "-b",
        "--numberoflinewiththenewline",
        action="store_true",
        help="Print number of lines with out the newline",
    )

    args = parser.parse_args()

    main(args)
