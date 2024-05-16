import sys
import pytest
from ..json_parser import main

def test_main(monkeypatch, capsys):
    # Mock the command-line arguments
    monkeypatch.setattr(sys, 'argv', ['json_parser.py', 'sample.json'])
    
    # Run the main function
    main()
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check the output
    assert captured.out == "Argument 1: hello, Argument 2: world\n"

