import subprocess
import os
import sys
import pytest
from io import StringIO

# Import main function from your script
from shell import main

SCRIPT_NAME = "shell.py"


@pytest.fixture
def run_script():
    """Fixture to run the shell script."""

    def _run_script(commands):
        # Create a subprocess to run the script
        proc = subprocess.Popen(
            [sys.executable, SCRIPT_NAME],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Send the commands to the script
        stdout, stderr = proc.communicate("\n".join(commands) + "\nexit\n")
        return stdout, stderr, proc.returncode

    return _run_script


def test_basic_command_execution(run_script):
    stdout, stderr, returncode = run_script(["echo Hello World"])
    assert "Hello World" in stdout
    assert returncode == 0


def test_directory_change(run_script):
    initial_dir = os.getcwd()
    test_dir = os.path.dirname(initial_dir)

    commands = [f"cd {test_dir}", "pwd"]

    stdout, stderr, returncode = run_script(commands)
    assert test_dir in stdout
    assert returncode == 0


def test_pipes_and_redirections(run_script):
    commands = [
        "echo Hello World > test_output.txt",
        "cat test_output.txt",
        "ls -la | grep test_output.txt",
    ]

    stdout, stderr, returncode = run_script(commands)
    assert "Hello World" in stdout
    assert "test_output.txt" in stdout
    assert returncode == 0

    # Clean up
    if os.path.exists("test_output.txt"):
        os.remove("test_output.txt")


def test_exit_script(run_script):
    stdout, stderr, returncode = run_script(["exit"])
    assert "Goodbye!" in stdout
    assert returncode == 0


# Import main function from your script
from shell import main

def test_command_history_output(monkeypatch):
    # Define commands to simulate user input
    commands = [
        "ls",
        "cd /path/to/directory",
        "echo Hello",
        "history",
    ]

    # TODO cannot seems to get stdin to talk to the main function
    # Patch sys.stdin to provide simulated user input
    monkeypatch.setattr('sys.stdin', StringIO('\n'.join(commands) + '\n'))

    # Patch sys.stdout to capture script output
    stdout = StringIO()
    sys.stdout = stdout

    # Run the main function
    main()

    # Get the output captured by sys.stdout during script execution
    output = stdout.getvalue()

    # Restore sys.stdout
    sys.stdout = sys.__stdout__

    # Assert that the output contains the command history
    assert "Command History:" in output
    assert "1. ls" in output
    assert "2. cd /path/to/directory" in output
    assert "3. echo Hello" in output
    assert "4. history" in output

