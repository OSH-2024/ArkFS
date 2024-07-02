import os

def open_image(file_path):
    try:
        if os.path.exists(file_path):
            os.startfile(file_path)  # For Windows
            # For macOS, use: subprocess.run(['open', file_path])
            # For Linux, use: subprocess.run(['xdg-open', file_path])
        else:
            print("File does not exist.")
    except Exception as e:
        print(f"Error opening file: {e}")

# Example usage
open_image("C:\programming\codefile\newgit\osh\类shell的文件系统\documents.txt")
