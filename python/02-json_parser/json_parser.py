import string
import re

def split_object(s):
    stack = []
    string_stack = []
    t = s[1:-1]
    for i, c in enumerate(t):
        if c == "[" and len(string_stack) == 0:
            stack.append("]")
        elif c == "{" and len(string_stack) == 0:       
            stack.append("}") 
        elif c == '"' and len(string_stack) > 0:
            string_stack.pop()
        elif c == '"':
            string_stack.append('"')
        elif c == "," and len(stack) != 0:
            # TODO super inefficent :(
            t = t[:i] + " " + t[i+1:]
        elif c == "]" and stack[-1] == "]":
            stack.pop()
        elif c == "}" and stack[-1] == "}":
            stack.pop()
        elif c == "]" and stack[-1] != "]":
            raise ValueError(f"Missing opening bracket")
        elif c == "}" and stack[-1] != "}":
            raise ValueError(f"Missing opening curly bracket")
    split_object = t.split(",")
    return [s.replace(" ", ",") for s in split_object]


def parse_object(obj, result_obj):
    if obj[0] != "{" or obj[-1] != "}":
        raise ValueError(f"String {obj} must be enclosed in curly brackets to be considered parsable")
    if len(obj) == 2:
        return {}
    for key_value_pair in split_object(obj):
        k_v = key_value_pair.split(":")
        if len(k_v) != 2:
            raise ValueError(f"{key_value_pair} is an invalid key value pair")
        key, value = k_v
        if not re.fullmatch(r'"[^"]+"', key):
            raise ValueError(f"{key} is an invalid key")
        else:
            key = key[1:-1]
        # TODO check for empty elements
        if value[0] == "{":
            o = parse_object(value, result_obj)
            result_obj[key] = o
        elif value[0] == "[":
            arr = parse_array(value, [])
            result_obj[key] = arr
        elif re.fullmatch(r'"[^"]+"', value):
            result_obj[key] = value[1:-1]
        elif re.fullmatch(r'\d+', value):
            result_obj[key] = int(value)
        else:
            raise ValueError(f"{value} is not a valid value")
    return result_obj

def parse_array(string, result_array):
    if string[0] != "[" or string[-1] != "]":
        raise ValueError(f"String {string} must be enclosed in brackets to be considered parsable")
    if len(string) == 2:
        return []
    for element in split_object(string):
        # TODO check for empty elements
        if element[0] == "{":
            o = parse_object(element, {})
            result_array.append(o)
        elif element[0] == "[":
            arr = parse_array(element, [])
            result_array.append(arr)
        elif re.fullmatch(r'"[^"]+"', element):
            result_array.append(element[1:-1])
        elif re.fullmatch(r'\d+', element):
            result_array.append(int(element))
        else:
            raise ValueError(f"{element} is not a valid value")
    return result_array

def main(s):
    sanitzed_string = "".join([c for c in s if c not in string.whitespace])
    return parse_object(sanitzed_string,{})
