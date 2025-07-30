from util import quicksort, merge_sort, radixsort, heapsort

test_arr = ["tan", "cat", "cat", "hello", "cato",
            "something", "something else", "foo", "bar", "baz"]
sorted_arr = test_arr[:]
sorted_arr.sort()
sorted_arr_str = str(sorted_arr)

print(str(radixsort(test_arr)))
print(str(merge_sort(test_arr)))


def test_quicksort():
    assert str(quicksort(test_arr)) == sorted_arr_str


def test_heapsort():
    assert str(heapsort(test_arr)) == sorted_arr_str


def test_mergesort():
    assert str(merge_sort(test_arr)) == sorted_arr_str


def test_radixsort():
    assert str(radixsort(test_arr)) == sorted_arr_str
