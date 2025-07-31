import heapq


def heapsort(arr):
    tmp = arr[:]
    result = []
    heapq.heapify(tmp)
    for _ in range(len(tmp)):
        result.append(heapq.heappop(tmp))
    return result


def merge_sort(arr):
    def merge(arr):
        if len(arr) == 1:
            return arr
        mid = len(arr) // 2
        left = merge(arr[:mid])
        right = merge(arr[mid:])
        return sort(left, right)

    def sort(p, q):
        merged = []
        a, b = 0, 0
        while not (a == len(p) and b == len(q)):
            if a == len(p):
                merged.append(q[b])
                b += 1
            elif b == len(q):
                merged.append(p[a])
                a += 1
            elif p[a] >= q[b]:
                merged.append(q[b])
                b += 1
            else:
                merged.append(p[a])
                a += 1
        return merged

    return merge(arr)


def radixsort(arr):

    max_digits = max([len(str(a)) for a in arr])
    max_ord_int = 0
    for string in arr:
        for char in string:
            max_ord_int = max(max_ord_int, ord(char))

    prefixed_array = [a.ljust(max_digits, "\0") for a in arr]
    map_prefixed_to_arr = {prefixed_array[i]: arr[i]
                           for i, _ in enumerate(prefixed_array)}

    for y in range(max_digits - 1, -1, -1):
        count = [0] * (max_ord_int + 1)

        for string in prefixed_array:
            a = ord(string[y])
            count[a] += 1

        count[0] -= 1
        for i, c in enumerate(range(len(count) - 1)):
            count[c + 1] += count[c]

        sorted = [0] * len(arr)

        for i in range(len(arr) - 1, -1, -1):
            val = prefixed_array[i]
            char = val[y]
            sorted[count[ord(char)]] = val
            count[ord(char)] -= 1

        prefixed_array = sorted

    return [map_prefixed_to_arr[a] for a in prefixed_array]


def quicksort(arr):
    stack = [(0, len(arr) - 1)]
    while stack:
        start, end = stack.pop()
        mid = start + (end - start) // 2
        arr[mid], arr[end] = arr[end], arr[mid]
        pivot_value = arr[end]
        left = start

        for i in range(start, end):
            if arr[i] < pivot_value:
                arr[i], arr[left] = arr[left], arr[i]
                left += 1

        arr[left], arr[end] = arr[end], arr[left]
        if start < left - 1:
            stack.append((start, left - 1))
        if left + 1 < end:
            stack.append((left + 1, end))

    return arr
