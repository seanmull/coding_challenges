from random import shuffle
import argparse
from util import quicksort, merge_sort, radixsort, heapsort

parser = argparse.ArgumentParser(
                    prog='sort',
                    description='Sorts text from file')
parser.add_argument('filename')           # positional argument
parser.add_argument('-u', '--unique',
                    action='store_true')  # on/off flag
parser.add_argument('-m', '--mergesort',
                    action='store_true')  # on/off flag
parser.add_argument('-q', '--quicksort',
                    action='store_true')  # on/off flag
parser.add_argument('-e', '--heapsort',
                    action='store_true')  # on/off flag
parser.add_argument('-r', '--radixsort',
                    action='store_true')  # on/off flag
parser.add_argument('-t', '--randomsort',
                    action='store_true')  # on/off flag


args = parser.parse_args()
num_of_sorts = sum([args.mergesort, args.quicksort, args.radixsort, args.randomsort, args.heapsort])
if num_of_sorts > 1:
    raise Exception("Choose one or none of the following sorts: --mergesort, --quicksort, --radixsort, --randomsort, --heapsort")

with open(args.filename, "r", encoding="utf-8") as file:
    input_stream = file.read()

unique = args.unique

lines = input_stream.split("\n")
if unique:
    lines = list(set(lines))

if args.quicksort:
    lines = quicksort(lines)
elif args.mergesort:
    lines = merge_sort(lines)
elif args.heapsort:
    lines = heapsort(lines)
elif args.radixsort:
    lines = radixsort(lines)
elif args.randomsort:
    lines = shuffle(lines)
else:
    lines = heapsort(lines)

for line in lines:
    print(line)
