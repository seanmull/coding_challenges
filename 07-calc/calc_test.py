from calc import evaluate_tokens
import pytest

def test_evaluate_simple_expression():
    assert evaluate_tokens("3 * 2") == 6

def test_evaluate_complex_expression():
    assert evaluate_tokens("5 * ( 4 - 2 + 2 ) - 6 / 3") == 18

def test_evaluate_expression_with_multiple_operators():
    assert evaluate_tokens("3 + 4 * 2 / ( 1 - 5 )") == 1

def test_evaluate_expression_with_division():
    assert evaluate_tokens("10 / 2") == 5

def test_evaluate_expression_with_all_operations():
    assert evaluate_tokens("10 + 3 * 5 / ( 16 - 4 )") == 11

def test_evaluate_single_number():
    assert evaluate_tokens("42") == 42

def test_evaluate_expression_with_large_numbers():
    assert evaluate_tokens("1000 + 2000 * 3000 + 4000") == 6005000

if __name__ == "__main__":
    pytest.main()
