import os

def list_files_in_folder(folder_path):
    files = []
    try:
        for root, _, filenames in os.walk(folder_path):
            for filename in filenames:
                files.append(os.path.join(root, filename))
    except Exception as e:
        print(f"An error occurred: {e}")
    return files
