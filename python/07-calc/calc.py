from collections import deque
import string
import re

# TODO add in parenthesis
# TODO deal with order of operations
# TODO deal with floating points
# TODO check what get passed into cmd look out for *

# expr1 = "1 * 2 - 3 * 4"
# expr = "4 * 9 + 3 / 2 - 67 * 54"
expr = "(4 * 9) + 3 / 2 - 67 * 54"
operators = set(["*", "-", "+", "/"])
# output = "4 9 * 3 2 / + 67 54 * -"

expr = "".join([c for c in expr if c not in string.whitespace])


operator_stack = []
output_queue = deque()


def evalute_expression(expr):
    tokens = []
    num = ""
    for s in expr:
        if re.match(r'\d', s):
            num += s
        elif re.match(r'[\*\/\+\-\(\)]', s):
            if num:
                tokens.append(num)
            num = ""
            tokens.append(s)
        else:
            raise Exception("Invalid character: " + s)

    if len(num) > 0:
        tokens.append(num)


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
                try:
                    x = b/a
                except ZeroDivisionError:
                    print("Error: Cannot divide by zero.")
        else:
            evaluate_stack.append(p)

    return evaluate_stack[0]
print(evalute_expression(expr))
