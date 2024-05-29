import threading
import time


def serialize_resp(value, string_type="simple"):
    if isinstance(value, str):
        if string_type == "simple":
            return f"+{value}\r\n"
        elif string_type == "bulk":
            return f"${len(value)}\r\n{value}\r\n"
    elif isinstance(value, int):
        return f":{value}\r\n"
    elif value is None:
        return f"$-1\r\n"
    elif isinstance(value, list):
        s = f"*{len(value)}\r\n"
        for v in value:
            s += f"${len(v)}\r\n{v}\r\n"
        return s
    elif isinstance(value, dict):
        if value["error"]:
            return f"-{value['error']}\r\n"


def deserialize_resp(data):
    if data.startswith("+"):
        return data[1:-2]
    elif data.startswith("-"):
        return {"error": data[1:-2]}
    elif data.startswith(":"):
        return int(data[1:-2])
    elif data.startswith("$"):
        if data == "$-1\r\n":
            return None
        data = data.split("\r\n")
        data = data[1:-1]
        return data[0]
    elif data.startswith("*"):
        data = data.split("\r\n")
        data = data[1:-1]
        data = list(filter(lambda x: not x.startswith("$"), data))
        return data


def deserialize_req(data):
    data = data.split("\r\n")
    data = data[1:-1]
    data = list(filter(lambda x: not x.startswith("$"), data))
    return data


def remove_key_after_delay(
    dictionary, key, delay_or_time, is_unix_time=False, is_milliseconds=False
):
    current_time = time.time()

    # Determine the delay
    if is_unix_time:
        # If given Unix time in milliseconds, convert it to seconds
        if is_milliseconds:
            target_time = delay_or_time / 1000.0
        else:
            target_time = delay_or_time
        delay = max(0, target_time - current_time)
    else:
        # If given delay in milliseconds, convert it to seconds
        if is_milliseconds:
            delay = delay_or_time / 1000.0
        else:
            delay = delay_or_time

    def remove_key():
        if key in dictionary:
            del dictionary[key]
            print(f"Key '{key}' has been removed after {delay} seconds.")
        else:
            print(f"Key '{key}' was not found in the dictionary.")

    timer = threading.Timer(delay, remove_key)
    timer.start()

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
