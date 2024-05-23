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

infix_tokens = args.expression.split(" ")

# Guidence for how to convert infix to postix https://www.andrew.cmu.edu/course/15-200/s06/applications/ln/junk.html

print(f"Infix tokens are {infix_tokens}")

stack = ["("]


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


precedence_table = {
    ")": {"stack": None, "input": 0},
    "(": {"stack": 0, "input": 5},
    "+": {"stack": 2, "input": 1},
    "-": {"stack": 2, "input": 1},
    "*": {"stack": 4, "input": 3},
    "/": {"stack": 4, "input": 3},
}

postfix_tokens = []


while len(infix_tokens) != 0:
    top = infix_tokens.pop(0)
    if is_int(top):
        postfix_tokens.append(top)
    elif top in ("(", ")","*", "/", "+", "-"):
        input_precedence = precedence_table[top]["input"]
        stack_precedence = precedence_table[stack[0]]["stack"]
        if stack_precedence >= input_precedence:
            topofstack = stack.pop()
            if topofstack not in ("("):
                postfix_tokens.append(topofstack)
        else:
            if top not in (")"):
                stack.append(top)
    else:
        print(f"{top} is a bad token.")
        exit()

print(postfix_tokens)

"""
Step 0: Initialize the stack by pushing a "(" -- this serves to mark the beginning of the stack and give it an initial precedence. Append a ")" to the input to pop the initial "(" from the stack.
Step 1: If the input is empty, go to Finished.
Step 2: Read one token (operand, parenthesis, operator) from the input.
Step 3: If the token is an operand, output it and goto Step 1.
Step 4: Look up the precedence of the input token in the "Input" column of the precedence table.
Step 5: Look up the precedence of the token on top of the stack in the "Stack" column of the precedence table.
Step 6: If the precedence of the top of the stack is greater than or equal to the precedence of the input, 
first pop the token off the 
top of the stack. If it is not a "(", output it. Either way, go to Step 5. 
Otherwise, if the precedence of the top of the stack is less than the precedence of the input, then if the input token is not a ")", 
push it onto the stack
Step 7: Go to Step 1.
Finished.
"""
