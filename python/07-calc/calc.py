from collections import deque
from decimal import DivisionByZero

# TODO deal with floating points
# TODO check for valiation of character used
# TODO check what get passed into cmd look out for *

expr = "1 * 2 - 3 * 4"
expr = "4 * 9 + 3 / 2 - 67 * 54"
operators = set(["*", "-", "+", "/"])
output = "4 9 * 3 2 / + 67 54 * -"


operator_stack = []
output_queue = deque()

tokens = expr.split(" ")

count = 0
for t in tokens:
    if t in operators:
        operator_stack.append(t)
    else:
        count += 1
        output_queue.append(int(t))
        if count % 2 == 0:
            while len(operator_stack) != 0:
                output_queue.append(operator_stack.pop())

while len(operator_stack) != 0:
    output_queue.append(operator_stack.pop())


evaluate_stack = []

while output_queue:
    p = output_queue.popleft()
    if p in operators:
        a = evaluate_stack.pop()
        b = evaluate_stack.pop()
        if p == "+":
            evaluate_stack.append(b + a)
        elif p == "-":
            evaluate_stack.append(b - a)
        elif p == "*":
            evaluate_stack.append(b * a)
        else:
            if a == 0 and b != 0:
                raise DivisionByZero(f'Cannot divide {b} by 0')
            else:
                evaluate_stack.append(b / a)
    else:
        evaluate_stack.append(p)


print(evaluate_stack[0])
