import os
import subprocess

def run_command(command):
    """Execute a shell command and print the output."""
    try:
        result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
        print(result.stdout, end='')
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

def main():
    while True:
        user_input = input(f"{os.getcwd()}$ ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        elif user_input.startswith('cd '):
            # Extract the path and change directory
            path = user_input[3:].strip()
            change_directory(path)
        else:
            # Run any other command
            run_command(user_input)
        # Flush stdout to ensure all output is immediately available
        sys.stdout.flush()

if __name__ == "__main__":
    import sys
    main()

