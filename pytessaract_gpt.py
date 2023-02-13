
import tkinter as tk
import openai
import pytesseract
from PIL import Image, ImageTk
import tkinter.filedialog

# Replace the value of `API_KEY` with your OpenAI API key
openai.api_key = "Your OpenAI Api Key"

# GUI
root = tk.Tk()
root.title("Book Summary")

frame = tk.Frame(root)
frame.pack(pady=10)

def select_image():
    file_path = tkinter.filedialog.askopenfilename()
    global img
    img = Image.open(file_path)

    # Run OCR on the image
    text = pytesseract.image_to_string(img)

    # Send the result to OpenAI's GPT-3 prompt
    model_engine = "text-davinci-002"
    prompt = f"Give Star Rating on the top based on your knowledge and then Create a New York Times review about the book titled: {text} "

    completions = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    display_image_and_summary(img, message)

def clear_all():
    image_label.destroy()
    summary_label.destroy()
    frame.pack_forget()
    frame.pack(pady=10)

def display_image_and_summary(img, message):
    global image_label, summary_label
    img = img.resize((img.width//2, img.height//2), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(img)
    image_label = tk.Label(frame, image=image)
    image_label.image = image
    image_label.pack(side=tk.LEFT, padx=10)

    summary_label = tk.Label(frame, text=message, font=("TkDefaultFont", 12), wraplength=500)
    summary_label.pack(side=tk.LEFT)

select_image_button = tk.Button(frame, text="Select Image", command=select_image)
select_image_button.pack(pady=10)

clear_all_button = tk.Button(frame, text="Clear All", command=clear_all)
clear_all_button.pack(pady=10)

root.mainloop()
