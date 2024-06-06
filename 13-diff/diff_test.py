import pytest
from utils import lcs, generate_diff


def test_lcs_empty_lists():
    assert lcs([], []) == {}


def test_lcs_one_empty_list():
    assert lcs(["A", "B", "C"], []) == {}
    assert lcs([], ["X", "Y", "Z"]) == {}


def test_lcs_no_common_subsequence():
    assert lcs(["A", "B", "C"], ["X", "Y", "Z"]) == {}


def test_lcs_entire_list_match():
    assert lcs(["A", "B", "C"], ["A", "B", "C"]) == {
        "A": [(0, 0)],
        "B": [(1, 1)],
        "C": [(2, 2)],
    }


def test_lcs_subsequence_at_beginning():
    assert lcs(["A", "B", "C", "D", "E", "F"], ["A", "B", "C", "X", "Y", "Z"]) == {
        "A": [(0, 0)],
        "B": [(1, 1)],
        "C": [(2, 2)],
    }


def test_lcs_subsequence_at_end():
    assert lcs(["X", "Y", "Z", "A", "B", "C"], ["D", "E", "F", "A", "B", "C"]) == {
        "A": [(3, 3)],
        "B": [(4, 4)],
        "C": [(5, 5)],
    }


def test_lcs_subsequence_in_middle():
    assert lcs(["A", "X", "B", "Y", "C", "Z"], ["A", "B", "C"]) == {
        "A": [(0, 0)],
        "B": [(2, 1)],
        "C": [(4, 2)],
    }


def test_lcs_identical_lists():
    assert lcs(["a", "b", "c"], ["a", "b", "c"]) == {
        "a": [(0, 0)],
        "b": [(1, 1)],
        "c": [(2, 2)],
    }


def test_lcs_permutation():
    assert lcs(["a", "b", "c"], ["a", "c", "b"]) == {"a": [(0, 0)], "c": [(2, 1)]}


def test_lcs_multiple_occurrences():
    assert lcs(["a", "b", "a"], ["a", "a", "b"]) == {"a": [(0, 0), (2, 1)]}


def test_lcs_long_common_subsequence():
    assert lcs(
        ["This is a test which contains:", "this is the lcs"],
        ["this is the lcs", "we're testing"],
    ) == {"this is the lcs": [(1, 0)]}


def test_lcs_multiple_long_common_subsequences():
    assert lcs(
        [
            "Coding Challenges helps you become a better software engineer through that build real applications.",
            "I share a weekly coding challenge aimed at helping software engineers level up their skills through deliberate practice.",
            "I’ve used or am using these coding challenges as exercise to learn a new programming language or technology.",
            "Each challenge will have you writing a full application or tool. Most of which will be based on real world tools and utilities.",
        ],
        [
            "Helping you become a better software engineer through coding challenges that build real applications.",
            "I share a weekly coding challenge aimed at helping software engineers level up their skills through deliberate practice.",
            "These are challenges that I’ve used or am using as exercises to learn a new programming language or technology.",
            "Each challenge will have you writing a full application or tool. Most of which will be based on real world tools and utilities.",
        ],
    ) == {
        "I share a weekly coding challenge aimed at helping software engineers level up their skills through deliberate practice.": [
            (1, 1)
        ],
        "Each challenge will have you writing a full application or tool. Most of which will be based on real world tools and utilities.": [
            (3, 3)
        ],
    }


def test_generate_diff_empty_lists():
    X = []
    Y = []
    common_lines = {}
    diff = generate_diff(X, Y, common_lines)
    expected_diff = ""
    assert diff == expected_diff


def test_generate_diff_identical_lists():
    X = ["A", "B", "C"]
    Y = ["A", "B", "C"]
    common_lines = lcs(X, Y)
    diff = generate_diff(X, Y, common_lines)
    expected_diff = "  A\n  B\n  C"
    assert diff == expected_diff


def test_generate_diff_subsequence_in_middle():
    X = ["A", "X", "B", "Y", "C", "Z"]
    Y = ["A", "B", "C"]
    common_lines = lcs(X, Y)
    diff = generate_diff(X, Y, common_lines)
    expected_diff = "  A\n< X\n  B\n< Y\n  C\n< Z"
    assert diff == expected_diff
