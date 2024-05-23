# BUBBLE_SORT
def bubbleSort(array):
    swapped = False
    for i in range(len(array)-1,0,-1):
        for j in range(i):
            if array[j]>array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                swapped= True
        if swapped:
            swapped=False
        else:
            break
    return array

# INSERTION_SORT
def insertionSort(array):
    for i in range(1, len(array)):
        key = array[i]
        j = i-1
        while array[j] > key and j >= 0:
            array[j+1] = array[j]
            j -= 1
        array[j+1] = key
    return array

# SELECTION_SORT
def selectionSort(array):
    for i in range(len(array)-1):
        min_idx = i
        for idx in range(i + 1, len(array)-1):
            if array[idx] < array[min_idx]:
                min_idx = idx
        array[i], array[min_idx] = array[min_idx], array[i]
    return array

# HEAP_SORT
def heapify(array, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and array[i] < array[l]:
        largest = l

    if r < n and array[largest] < array[r]:
        largest = r

    if largest != i:
        array[i], array[largest] = array[largest], array[i]
        heapify(array, n, largest)
        
def heapSort(array):
    n = len(array)
    for i in range(n//2, -1, -1):
        heapify(array, n, i)
    for i in range(n-1, 0, -1):
        array[i], array[0] = array[0], array[i]
        heapify(array, i, 0)
    return array

# MERGE_SORT
def mergeSort(nums):
    if len(nums)==1:
        return nums
    mid = (len(nums)-1) // 2
    lst1 = mergeSort(nums[:mid+1])
    lst2 = mergeSort(nums[mid+1:])
    result = merge(lst1, lst2)
    return result

def merge(lst1, lst2):
    lst = []
    i = 0
    j = 0
    while(i<=len(lst1)-1 and j<=len(lst2)-1):
        if lst1[i]<lst2[j]:
            lst.append(lst1[i])
            i+=1
        else:
            lst.append(lst2[j])
            j+=1
    if i>len(lst1)-1:
        while(j<=len(lst2)-1):
            lst.append(lst2[j])
            j+=1
    else:
        while(i<=len(lst1)-1):
            lst.append(lst1[i])
            i+=1
    return lst   

# QUICK_SORT
def quickSort(array):
    if len(array)> 1:
        pivot=array.pop()
        grtr_lst, equal_lst, smlr_lst = [], [pivot], []
        for item in array:
            if item == pivot:
                equal_lst.append(item)
            elif item > pivot:
                grtr_lst.append(item)
            else:
                smlr_lst.append(item)
        return (quickSort(smlr_lst) + equal_lst + quickSort(grtr_lst))
    else:
        return array

#SHELL_SORT
def shellSort(array):
    n = len(array)
    interval = n // 2
    while interval > 0:
        for i in range(interval, n):
            temp = array[i]
            j = i
            while j >= interval and array[j - interval] > temp:
                array[j] = array[j - interval]
                j -= interval

            array[j] = temp
        interval //= 2
    return array
def counting_sort_for_radix(arr, exp, max_unicode):
    n = len(arr)
    output = [0] * n
    count = [0] * (max_unicode + 2)  # Plus one for padding, plus one for range

    # Store count of occurrences of each character
    for i in range(n):
        index = ord(arr[i][exp]) if exp < len(arr[i]) else 0
        count[index + 1] += 1  # Increment count at index + 1 to handle padding

    # Change count[i] so that count[i] contains the actual position of this character in output
    for i in range(1, max_unicode + 2):
        count[i] += count[i - 1]

    # Build the output array
    for i in range(n - 1, -1, -1):
        index = ord(arr[i][exp]) if exp < len(arr[i]) else 0
        output[count[index + 1] - 1] = arr[i]
        count[index + 1] -= 1

    # Copy the output array to arr
    for i in range(n):
        arr[i] = output[i]

def radixSort(arr):
    # Find the maximum length of word in the list
    max_len = max(len(word) for word in arr)
    
    # Find the maximum Unicode code point in the list
    max_unicode = max(ord(char) for word in arr for char in word)

    # Normalize the length of words by padding with '\0' (null character)
    padded_arr = [word.ljust(max_len, '\0') for word in arr]

    # Perform counting sort for each digit (character) from the least significant to most significant
    for exp in range(max_len - 1, -1, -1):
        counting_sort_for_radix(padded_arr, exp, max_unicode)

    # Remove the padding
    sorted_arr = [word.rstrip('\0') for word in padded_arr]
    return sorted_arr

def randomSort(arr):
    import random
    nums = list(range(0, len(arr)))
    random.shuffle(nums)
    for i, ele in enumerate(arr):
        arr[nums[i]] = arr[i]
    return arr
