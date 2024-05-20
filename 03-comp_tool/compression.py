import sys

args = sys.argv


def main():

    file = open(sys.argv[1], "r")

    content = file.read()

    m = create_freq_map(content)

    print(m)

def create_freq_map(str):
    map = {}
    for char in str:
        if char in map:
            map[char] += 1
        else:
            map[char] = 1
    return map


if __name__ == "__main__":
    main()
