import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pytesseract

def process_image():
    try:
        # Open file dialog to select an image file
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        
        if not filepath:
            return

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(Image.open(filepath), lang='khm')

        # Display the extracted text in the text widget
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, extracted_text)
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Khmer Text Extractor")
root.geometry("600x400")
root.configure(bg="#121212")

# Create a label for the title
title_label = tk.Label(root, text="Khmer Text Extractor", font=("Arial", 20), fg="white", bg="#121212")
title_label.pack(pady=10)

# Create a button to select an image file
select_button = tk.Button(root, text="Select Image", command=process_image, bg="#303030", fg="white")
select_button.pack(pady=10)

# Create a text widget to display the extracted text
text_widget = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#303030", fg="white")
text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a scrollbar for the text widget
scrollbar = tk.Scrollbar(text_widget)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Run the Tkinter event loop
root.mainloop()
