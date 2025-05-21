from tkinterdnd2 import DND_FILES, TkinterDnD
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageEnhance
import pytesseract
from googletrans import Translator
from tkinter import ttk

# Global variables
translator = Translator()
current_text = {"original": "", "translated": "", "is_mixed": False}

def toggle_language():
    # Simple toggle between original and translated text
    if text_widget.get("1.0", tk.END).strip() == current_text["original"].strip():
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, current_text["translated"])
        toggle_button.config(text="Show Original")
    else:
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, current_text["original"])
        toggle_button.config(text="Show Translation")

def handle_drop(event, lang):
    # Get the dropped file path
    try:
        file_path = event.data
        if file_path.startswith('{'):  # Windows workaround
            file_path = file_path.strip('{}')
        process_image(6, lang, file_path)
        event.widget.configure(bg="#303030")  # Reset color
    except Exception as e:
        messagebox.showerror("Error", str(e))

def handle_drag_enter(event):
    event.widget.configure(bg="#505050")  # Highlight effect

def handle_drag_leave(event):
    event.widget.configure(bg="#303030")  # Reset color

def process_image(psm_mode, lang, filepath=None):
    try:
        if filepath is None:
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
        extracted_text = pytesseract.image_to_string(image, lang=lang, config=f'--psm {psm_mode}')
        
        # Store original text
        current_text["original"] = extracted_text
        current_text["is_mixed"] = (lang == 'khm+eng')

        # Translate text based on the language mode
        if lang == 'khm':
            current_text["translated"] = translator.translate(extracted_text, src='km', dest='en').text
        elif lang == 'eng':
            current_text["translated"] = translator.translate(extracted_text, src='en', dest='km').text
        elif lang == 'khm+eng':
            current_text["translated"] = translator.translate(extracted_text, src='km', dest='en').text

        # Display the original text
        text_widget.delete('1.0', tk.END)
        text_widget.insert(tk.END, current_text["original"])
        
        # Show toggle button for all modes
        toggle_button.pack(pady=5)
        separator.pack(fill='x', padx=10, pady=5)
        toggle_button.config(text="Show Translation")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# Create the main window
root = TkinterDnD.Tk()
root.title("Text Extractor")
root.geometry("600x500")
root.configure(bg="#121212")

# Create a label for the title
title_label = tk.Label(root, text="Text Extractor", font=("Arial", 20), fg="white", bg="#121212")
title_label.pack(pady=10)

# Create a frame for the buttons
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

# Create buttons to select the page segmentation mode and language
khmer_button = tk.Button(button_frame, text="Khmer", command=lambda: process_image(6, 'khm'), bg="#303030", fg="white", width=15, height=2, font=("Helvetica", 12))
khmer_button.pack(side=tk.LEFT, padx=10)

english_button = tk.Button(button_frame, text="English", command=lambda: process_image(6, 'eng'), bg="#303030", fg="white", width=15, height=2, font=("Helvetica", 12))
english_button.pack(side=tk.LEFT, padx=10)

khmer_english_button = tk.Button(button_frame, text="Khmer and English", command=lambda: process_image(6, 'khm+eng'), bg="#303030", fg="white", width=20, height=2, font=("Helvetica", 12))
khmer_english_button.pack(side=tk.LEFT, padx=10)

# Create a text widget to display the extracted text
text_widget = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#303030", fg="white", height=20)
text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a scrollbar for the text widget
scrollbar = tk.Scrollbar(text_widget)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_widget.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_widget.yview)

# Create toggle button and separator
toggle_button = tk.Button(root, text="Show Translation", command=toggle_language, 
                         bg="#303030", fg="white", width=15, height=1, font=("Helvetica", 10))
toggle_button.pack_forget()

# Create separator line
separator = tk.Frame(root, height=2, bg="#404040")
separator.pack_forget()

# Create buttons with drag and drop
for btn, txt, lng in [
    (khmer_button, "Khmer", 'khm'),
    (english_button, "English", 'eng'),
    (khmer_english_button, "Khmer and English", 'khm+eng')
]:
    btn.drop_target_register('DND_Files')
    btn.dnd_bind('<<Drop>>', lambda e, l=lng: handle_drop(e, l))
    btn.dnd_bind('<<DragEnter>>', handle_drag_enter)
    btn.dnd_bind('<<DragLeave>>', handle_drag_leave)

# Add hint label
hint_label = tk.Label(root, 
                     text="Tip: Drag and drop images onto buttons to process",
                     font=("Arial", 9, "italic"), 
                     fg="#808080", 
                     bg="#121212")

hint_label.pack(pady=(0, 10))
# Run the Tkinter event loop
root.mainloop()
