import sys
from json_parser import main

def __eq__(self, other):
    if isinstance(self, other.__class__):
        return self.a == other.a and self.b == other.b
    return False

def test_success(monkeypatch):
    # Mock the command-line arguments
    monkeypatch.setattr(sys, "argv", ["json_parser.py", "sample.json"])

    # Run the main function
    actual_output = main()

    expected_output = {
        "key1": True,
        "key2": False,
        "key3": None,
        "key4": "value",
        "key5": 101,
        "key6": {},
    }

    # Check the output
    assert actual_output == expected_output

def test_failure(monkeypatch, capsys):
    # Mock the command-line arguments
    monkeypatch.setattr(sys, "argv", ["json_parser.py", "invalid_sample.json"])

    # Run the main function
    main()

    captured = capsys.readouterr()

    # Check the output
    assert captured.out == "The json file is invalid.\n"
