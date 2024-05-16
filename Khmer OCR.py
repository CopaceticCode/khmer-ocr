import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import pytesseract

def process_image(psm_mode):
    try:
        # Open file dialog to select an image file
        filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp")])
        if not filepath:
            return

        # Open the image
        image = Image.open(filepath)

        # Enhance image contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(2.0)

        # Convert the image to grayscale
        image = image.convert('L')

        # Use pytesseract to extract text from the image
        extracted_text = pytesseract.image_to_string(image, lang='khm', config=f'--psm {psm_mode}')

        # Display the extracted text in the text widget
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, extracted_text)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = tk.Tk()
root.title("Khmer Text Extractor")
root.geometry("600x500")
root.configure(bg="#121212")

# Create a label for the title
title_label = tk.Label(root, text="Khmer Text Extractor", font=("Arial", 20), fg="white", bg="#121212")
title_label.pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

# Create buttons to select the page segmentation mode
uniform_button = tk.Button(button_frame, text="Uniform Text (psm 6)", command=lambda: process_image(6), bg="#303030", fg="white")
uniform_button.pack(side=tk.LEFT, padx=10)

sparse_button = tk.Button(button_frame, text="Sparse Text (psm 11)", command=lambda: process_image(11), bg="#303030", fg="white")
sparse_button.pack(side=tk.LEFT, padx=10)

# Create a text widget to display the extracted text
text_widget = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#303030", fg="white", height=20)
text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a scrollbar for the text widget
scrollbar = tk.Scrollbar(text_widget)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Run the Tkinter event loop
root.mainloop()
