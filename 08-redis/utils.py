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
