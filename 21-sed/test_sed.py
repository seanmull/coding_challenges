import pytest
import os
import subprocess
import sys

# Get the directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to sed.py
sed_script = os.path.join(current_dir, "sed.py")


@pytest.fixture
def text_file_path(tmpdir):
    # Create a temporary text file with the provided content
    content = '''"Your heart is the size of an ocean. Go find yourself in its hidden depths."
"The Bay of Bengal is hit frequently by cyclones. The months of November and May, in particular, are dangerous in this regard."
"Thinking is the capital, Enterprise is the way, Hard Work is the solution."
"If You Can'T Make It Good, At Least Make It Look Good."
"Heart be brave. If you cannot be brave, just go. Love's glory is not a small thing."
"It is bad for a young man to sin; but it is worse for an old man to sin."
"If You Are Out To Describe The Truth, Leave Elegance To The Tailor."
"O man you are busy working for the world, and the world is busy trying to turn you out."
"While children are struggling to be unique, the world around them is trying all means to make them look like everybody else."
"These Capitalists Generally Act Harmoniously And In Concert, To Fleece The People."'''
    file_path = tmpdir.join("text.txt")
    file_path.write(content)
    yield str(file_path)  # Provide the file path to the test function
    file_path.remove()  # Clean up the temporary file after the test


def test_substitution_flag(text_file_path):
    print("Current working directory:", os.getcwd())
    print("Python executable path:", sys.executable)
    subprocess.run(["python3", sed_script, "s/o/O/g", text_file_path, "-i"])
    with open(text_file_path) as file:
        content = file.read()
        assert "Ocean" in content
        assert "ocean" not in content


def test_print_pattern_flag(text_file_path):
    result = subprocess.run(
        ["python3", sed_script, "/brave/p", text_file_path],
        capture_output=True,
        text=True,
    )
    assert "brave" in result.stdout
    assert "unique" not in result.stdout


def test_double_space_flag(text_file_path):
    result = subprocess.run(
        ["python3", sed_script, "/brave/p", text_file_path, "-G"],
        capture_output=True,
        text=True,
    )
    lines = result.stdout.split("\n")
    # Count empty lines
    empty_line_count = sum(1 for line in lines if line == "")
    assert (
        empty_line_count == (len(lines) - 1) // 2
    )  # Ensure there is an empty line after each matched line


def test_edit_in_place_flag(text_file_path):
    subprocess.run(["python3", sed_script, "s/o/O/g", text_file_path, "-i"])
    with open(text_file_path) as file:
        content = file.read()
        assert "Ocean" in content
        assert "ocean" not in content


def test_stdin_stdout():
    input_data = '''"Your heart is the size of an ocean. Go find yourself in its hidden depths."'''
    result = subprocess.run(
        ["python3", sed_script, "s/o/O/g"],
        input=input_data,
        capture_output=True,
        text=True,
    )
    assert "Ocean" in result.stdout
    assert "ocean" not in result.stdout


def test_file_stdout(text_file_path):
    result = subprocess.run(
        ["python3", sed_script, "s/o/O/g", text_file_path],
        capture_output=True,
        text=True,
    )
    assert "Ocean" in result.stdout
    assert "ocean" not in result.stdout


def test_file_edit_in_place(text_file_path):
    subprocess.run(["python3", sed_script, "s/o/O/g", text_file_path, "-i"])
    with open(text_file_path) as file:
        content = file.read()
        assert "Ocean" in content
        assert "ocean" not in content
