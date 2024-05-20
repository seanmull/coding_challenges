import sys
import pytest
from myscript import main

def test_main(monkeypatch, capsys):
    # Mock the command-line arguments
    monkeypatch.setattr(sys, 'argv', ['myscript.py', 'hello', 'world'])
    
    # Run the main function
    main()
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check the output
    assert captured.out == "Argument 1: hello, Argument 2: world\n"

def test_main_no_args(monkeypatch, capsys):
    # Mock the command-line arguments with no arguments
    monkeypatch.setattr(sys, 'argv', ['myscript.py'])
    
    # Run the main function and check for SystemExit
    with pytest.raises(SystemExit):
        main()
    
    # Capture the output
    captured = capsys.readouterr()
    
    # Check the output
    assert captured.out == "Usage: myscript.py <arg1> <arg2>\n"

