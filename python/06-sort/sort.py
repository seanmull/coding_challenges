
with open("pg132.txt", "r", encoding="utf-8") as file:
    input_stream = file.read()

unique = True

lines = input_stream.split("\n")
if unique:
    lines = list(set(lines))
lines.sort()

pass
