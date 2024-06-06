import os
import subprocess
import sys

command_history = []  # List to store command history

def run_command(command):
    """Execute a shell command and print the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        output = result.stdout
        print(output, end='')
        return output
    except subprocess.CalledProcessError:
        # Suppress the error message to mimic shell behavior
        pass

def change_directory(path):
    """Change the current working directory."""
    try:
        os.chdir(path)
        print(f"Changed directory to: {os.getcwd()}")
    except Exception as e:
        print(f"Error changing directory: {e}")

def show_history():
    """Show the command history."""
    print("Command History:")
    for idx, cmd in enumerate(command_history, start=1):
        print(f"{idx}. {cmd}")

def main():
    while True:
        user_input = input(f"{os.getcwd()}$ ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'history':
            show_history()
            command_history.append(user_input)  # Add 'history' command to history
        elif user_input.startswith('cd '):
            # Extract the path and change directory
            path = user_input[3:].strip()
            change_directory(path)
            command_history.append(user_input)  # Add 'cd' command to history
        else:
            output = run_command(user_input)
            command_history.append(user_input)  # Add command to history if executed
        # Flush stdout to ensure all output is immediately available
        sys.stdout.flush()

if __name__ == "__main__":
    main()

