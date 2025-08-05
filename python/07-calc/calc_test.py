from calc import evalute, convert_to_polish
import pytest

EMPTY_EXPRESSION = ""
SINGLE_NUMBER = "1"
VALID_WITHOUT_PARA = "4 * 9 + 3 / 2 - 67 * 54"
VALID_WITH_PARA = "4 * (9 + 3) / 2 - 6 * 5"
ORDER_OF_OPERATIONS1 = "4 * 3 + 2"
ORDER_OF_OPERATIONS2 = "4 + 3 * 2"
MIX_FLOAT_AND_INT = "1 + 2.1231232321321313"

INVALID_SPLIT_NUMS = "1 1 + 2"
INVALID_TWO_OPERATORS = "1 + - 1"
DIVIDE_BY_ZERO = "4 / 0"
NOT_CLOSED_PARA = "4 * (9 + 3 / 2 - 6 * 5"


def test_empty_expression():
    assert 0 == evalute(EMPTY_EXPRESSION)


def test_single_number():
    assert 1 == evalute(SINGLE_NUMBER)


def test_without_para():
    _, polish_notation = convert_to_polish(VALID_WITHOUT_PARA.split(" "))
    assert "4 9 * 3 2 / + 67 54 * -" == polish_notation


def test_with_para():
    assert -6.0 == evalute(VALID_WITH_PARA)


def test_order1():
    assert 14 == evalute(ORDER_OF_OPERATIONS1)


def test_order2():
    assert 10 == evalute(ORDER_OF_OPERATIONS2)


def test_float_int():
    assert 3.1231232321321313 == evalute(MIX_FLOAT_AND_INT)


def test_split_numbers():
    with pytest.raises(Exception):
        evalute(INVALID_SPLIT_NUMS)


def test_invalid_operators():
    with pytest.raises(Exception):
        evalute(INVALID_TWO_OPERATORS)


def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        evalute(DIVIDE_BY_ZERO)


def test_not_closed_para():
    with pytest.raises(Exception):
        evalute(NOT_CLOSED_PARA)
