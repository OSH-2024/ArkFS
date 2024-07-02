import tkinter as tk
from PIL import Image, ImageTk

def open_new_window_with_text_and_image(text, image_path):
    # Create a new Tkinter window
    window = tk.Tk()
    window.title("Display Text and Image")

    # Add a label for displaying text
    label_text = tk.Label(window, text=text, padx=20, pady=20, wraplength=400)
    label_text.pack()

    # Load and display an image
    if image_path:
        image = Image.open(image_path)
        image = image.resize((300, 300), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(image)
        label_image = tk.Label(window, image=photo)
        label_image.image = photo  # keep a reference
        label_image.pack()

    # Run the Tkinter main loop
    window.mainloop()

# Example usage
text_to_display = "Hello, this is some text to display."
image_file = "/home/fengli-osh/osh/LabelMatching/target_folder/AIserver.png"  # Replace with your image file path
open_new_window_with_text_and_image(text_to_display, image_file)
