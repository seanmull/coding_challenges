import argparse
from signal import signal, SIGPIPE, SIG_DFL  
signal(SIGPIPE,SIG_DFL) 
import algo
# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Sorts through words.")

parser.add_argument(
        "filename", 
        type=str, 
        nargs="?", 
        help="File you want to readin.")

parser.add_argument(
    "-u",
    "--unique",
    action="store_true",
    help="flag for unique char",
)

parser.add_argument(
    "-s",
    "--sorting_algo",
    type=str,
    help="Choosing the type of algo you want to use",
)

allowed_algos = ("radixsort", "quicksort", "mergesort", "heapsort", "randomsort")

args = parser.parse_args()

if not args.sorting_algo: 
    args.sorting_algo = "quicksort"
elif not args.sorting_algo in allowed_algos:
    print(f"{args.sorting_algo} is not an allowed algo to use.")
    exit()

if args.filename:
    file = open(args.filename, 'r')
else:
    import sys
    file = sys.stdin

content = file.read()

words = content.split("\n")

if args.unique:
    words = list(set(words))

algo_arg = args.sorting_algo

if algo_arg == "radixsort":
    words = algo.radixSort(words)
elif algo_arg == "quicksort":
    words = algo.quickSort(words)
elif algo_arg == "mergesort":
    words = algo.mergeSort(words)
elif algo_arg == "randomsort":
    words = algo.randomSort(words)
else:
    words = algo.heapSort(words)

words.sort()

for word in words:
    if len(word) > 0:
        print(word)
