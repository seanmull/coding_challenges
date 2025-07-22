import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def print_number(number):
    time.sleep(1)
    print(f'The number for this function execution is {number}')
    return number + 1

# map to get the results without having to strip away the future object
with ThreadPoolExecutor() as executor:
    results = executor.map(print_number, [1,2,3,4])
    print(list(results))

    
def print_hello(name):
    return f'Hello {name}'

# simple use case
with ThreadPoolExecutor() as executor:
    future1 = executor.submit(print_hello, "Sean")
    future2 = executor.submit(print_hello, "John")
    result1 = future1.result() 
    result2 = future2.result()
    # print(result1, result2)

# for when we want results when they become available
with ThreadPoolExecutor() as executor:
    future1 = executor.submit(print_hello, "Sean")
    future2 = executor.submit(print_hello, "John")
    futures = [future1, future2]
    for f in as_completed(futures):
        print(f.result())
    # result1 = future1.result() 
    # result2 = future2.result()
    # print(result1, result2)
