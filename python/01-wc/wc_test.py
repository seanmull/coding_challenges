# content of test_sample.py
from wc import calculate_counts

TEST_STRING = "hello world\nthis is awesome\ntwo  spaces\n"
number_of_lines, number_of_words, number_of_bytes, number_of_char, _ = calculate_counts(TEST_STRING)

def test_number_of_lines():
    assert number_of_lines == 3

def test_number_of_words():
    assert number_of_words == 7

def test_number_of_bytes():
    assert number_of_bytes == 40

def test_number_of_char():
    assert number_of_char == 41
