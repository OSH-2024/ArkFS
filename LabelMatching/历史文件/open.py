import os
import subprocess

def open_file_in_explorer(file_path):
    if os.path.exists(file_path):
        # Using the subprocess module to open the file with the default file explorer
        subprocess.run(['explorer', '/select,', file_path])
    else:
        print(f"The file {file_path} does not exist.")

# Example usage
file_path = r'C:\programming\codefile\newgit\osh\LabelMatching\target_folder\AIserver.png'
open_file_in_explorer(file_path)
