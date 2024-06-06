import subprocess
import os
import sys
import pytest

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
            text=True
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
    
    commands = [
        f"cd {test_dir}",
        "pwd"
    ]
    
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

