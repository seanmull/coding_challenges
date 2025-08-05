from collections import deque
import string
import re

# TODO deal with negative numbers

operators = set(["*", "-", "+", "/"])
precedence = {
    "*": 3,
    "/": 3,
    "+": 2,
    "-": 2
}
regex = r'\(*[0-9]\.?[0-9]*(\s*[*/+-]\s*\(*[0-9]\.?[0-9]*\)*)*'


def convert_to_polish(tokens):
    operator_stack = []
    output_queue = deque()
    for t in tokens:
        if t in operators and len(operator_stack) == 0:
            operator_stack.append(t)
        elif t in operators:
            while (operator_stack and
                   precedence[t] <= precedence[operator_stack[-1]]):
                output_queue.append(operator_stack.pop())
            operator_stack.append(t)
        else:
            if re.search(r'\.', t):
                output_queue.append(float(t))
            else:
                output_queue.append(int(t))

    while len(operator_stack) != 0:
        output_queue.append(operator_stack.pop())
    return output_queue, " ".join([str(s) for s in list(output_queue)])


def evalute_expression(expr):
    tokens = []
    num = ""
    for s in expr:
        if re.match(r'[0-9.]', s):
            num += s
        elif re.match(r'[\*\/\+\-\(\)]', s):
            if num:
                tokens.append(num)
            num = ""
            tokens.append(s)
    if len(num) > 0:
        tokens.append(num)

    output_queue, _ = convert_to_polish(tokens)

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
                    evaluate_stack.append(x)
                except ZeroDivisionError:
                    raise ZeroDivisionError("Error: Cannot divide by zero.")
        else:
            evaluate_stack.append(p)
    return evaluate_stack[0]


def evalute(expr):

    if len(expr) == 0:
        return 0

    if not re.fullmatch(regex, expr):
        raise Exception(
            "Expression has invalid format. <number><operator><number>...")

    expr = "".join([c for c in expr if c not in string.whitespace])

    para_stack = []
    for e in expr:
        if e == ")":
            if para_stack[-1] == "(":
                para_stack.pop()
            else:
                raise Exception("Lack of opening or closing paranthesis")
        elif e == "(":
            para_stack.append(e)
    if len(para_stack) != 0:
        raise Exception("Lack of opening or closing paranthesis")

    split_expressions = re.split(r'[()]', expr)
    for i, e in enumerate(split_expressions):
        if re.fullmatch(regex, e):
            split_expressions[i] = str(evalute_expression(e))
    revised_expression = "".join(split_expressions)
    return evalute_expression(revised_expression)
