import heapq
arr = [2, 4, 1, 3, 5, -1, 3, 9, 10, 11, 1, 67, 43]

# TODO run some tests to compare this to the sort().  also need to check strings, radix sort will need to be edited to handle strings


def heapsort(arr):
    result = []
    heapq.heapify(arr)
    for _ in range(len(arr)):
        result.append(heapq.heappop(arr))
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

    def get_digit(number, n):
        return (number // 10**n) % 10

    for y in range(max_digits):
        count = [0] * 10

        for a in arr:
            a = get_digit(a, y)
            count[a] += 1

        count[0] -= 1
        for i, c in enumerate(range(len(count) - 1)):
            count[c + 1] = count[c + 1] + count[c]

        sorted = [0] * len(arr)

        for i in range(len(arr) - 1, -1, -1):
            val = arr[i]
            digit = get_digit(val, y)
            sorted[count[digit]] = val
            count[digit] -= 1

        arr = sorted

    return arr


def quicksort(arr):
    def dfs(start, end):
        if start >= end:
            return
        pivot = get_pivot(start, end)
        dfs(start, pivot - 1)
        dfs(pivot + 1, end)

    def get_pivot(start, end):
        mid = start + (end - start) // 2
        arr[mid], arr[end] = arr[end], arr[mid]
        pivot_value = arr[end]
        left = start

        for i in range(start, end):
            if arr[i] < pivot_value:
                arr[i], arr[left] = arr[left], arr[i]
                left += 1

        arr[left], arr[end] = arr[end], arr[left]
        return left

    dfs(0, len(arr) - 1)
    return arr
