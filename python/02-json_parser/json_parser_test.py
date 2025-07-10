from json_parser import main

s = '{"k[ey": "value","key-n":101,"key-o":{},"key-l":[1,2,3,[4,5]]}'

obj = main(s)

def test_first_key_with_bracket():
    assert obj["k[ey"]

def test_integer():
    assert obj["key-n"] == 101

def test_array_value():
    assert obj["key-l"][3][1] == 5

