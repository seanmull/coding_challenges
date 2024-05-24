import argparse

# Good description on how to use argparse https://www.bitecode.dev/p/parameters-options-and-flags-for

parser = argparse.ArgumentParser(description="Simple calculator cli")

parser.add_argument("expression", type=str, help="Expression passed through")

args = parser.parse_args()

if args.expression:
    input = args.expression
else:
    import sys

    input = sys.stdin

# shunting yard algo
def infix_to_postfix(expression):
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '(': 0}
    output = []
    operators = []

    def is_operator(c):
        return c in precedence

    def greater_precedence(op1, op2):
        return precedence[op1] > precedence[op2]

    tokens = expression.split()
    for token in tokens:
        if token.isnumeric():  # If the token is an operand (number), add it to the output list
            output.append(token)
        elif token == '(':  # If the token is '(', push it to the stack
            operators.append(token)
        elif token == ')':  # If the token is ')', pop and output from the stack until '(' is found
            top_token = operators.pop()
            while top_token != '(':
                output.append(top_token)
                top_token = operators.pop()
        else:  # If the token is an operator, pop from the stack to the output until the stack is empty, or the operator at the top of the stack has less precedence than the current token
            while (operators and not greater_precedence(token, operators[-1])):
                output.append(operators.pop())
            operators.append(token)
    
    # Pop all the remaining operators in the stack to the output
    while operators:
        output.append(operators.pop())

    return output

def calc(postfix_tokens):
    stack = []
    while(len(postfix_tokens) != 0):
        top = postfix_tokens.pop(0)
        if top.isnumeric():
            stack.append(top)
        else:
            second = int(stack.pop())
            first = int(stack.pop())
            if top == "+":
                stack.append(first + second)
            elif top == "-":
                stack.append(first - second)
            elif top == "*":
                stack.append(first * second)
            elif top == "/":
                try:
                    print(first/second)
                except ZeroDivisionError as e:
                    print("Error: Cannot divide by zero")
                stack.append(first / second)
    return int(stack[0])

def evaluate_tokens(input):
    postfix_tokens = infix_to_postfix(input)
    return calc(postfix_tokens)
